from __future__ import unicode_literals

import threading
import sys
import logging

from messenger_api.MessengerAPI.utils.universal_type_checking import is_integer
from messenger_api.MessengerAPI.Messenger import Messenger
from messenger_api.MessengerAPI.Message import Message
from messenger_api.MessengerAPI.Thread import Thread
from .PluginLoader import PluginLoader
from .Command import Command

if sys.version_info >= (3, 0):
    # noinspection PyUnresolvedReferences
    from queue import Queue
else:
    # noinspection PyUnresolvedReferences
    from Queue import Queue


__author__ = 'JuniorJPDJ'

logger = logging.getLogger(__name__)


class MessengerBot(object):
    class QueueThread(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init__(self, daemon=True)
            self.queue = queue

        def run(self):
            while True:
                self.queue.get()()
                self.queue.task_done()

    def __init__(self, bot_username, bot_password, threads=None, command_startswith='!', plugins_dir='plugins'):
        """
        :type bot_username: str
        :type bot_password: str
        :type threads: iterable of ints
        :type command_startswith: str
        :type plugins_dir: str
        """
        self.__commands = []
        self.queue = Queue()
        self.queue_thread = self.QueueThread(self.queue)
        self.queue_thread.start()

        self.threads = []
        self.command_startswith = command_startswith
        self.msg = Messenger(bot_username, bot_password)

        if threads is not None:
            for t in threads:
                if is_integer(t):
                    self.threads.append(self.msg.get_thread(t))

        self.msg.register_action_handler(Message, self._run_command)

        self.plugin_loader = PluginLoader(plugins_dir, bot=self)
        self.plugin_loader.load_plugins()

        logger.info('Started')

    def add_thread(self, thread):
        """
        :type thread: Thread
        """
        assert isinstance(thread, Thread)
        self.threads.append(thread)

    def pull(self):
        logger.debug('Pulling!')
        return self.msg._pparser.make_pull()

    def register_command(self, command):
        """
        :type command: Command
        """
        assert isinstance(command, Command)
        self.__commands.append(command)

    def _parse_args(self, msg):
        """
        :type msg: Message
        """

        if msg.thread not in self.threads or not msg.body.startswith(self.command_startswith)\
           or len(msg.body) == 1 or msg.author == self.msg.me:
            return

        args = ['']
        quote_mode = False
        double_quote_mode = False
        escape_mode = False
        for char in msg.body:
            if escape_mode:
                args[-1] += char
                escape_mode = False
            elif char == ' ' and not (quote_mode or double_quote_mode):
                args.append('')
            elif char == "'" and not double_quote_mode:
                quote_mode = not quote_mode
            elif char == '"' and not quote_mode:
                double_quote_mode = not double_quote_mode
            elif char == '\\' and not (quote_mode or double_quote_mode):
                escape_mode = True
            else:
                args[-1] += char

        return args

    def _run_command(self, msg):
        """
        :type msg: Message
        """
        args = self._parse_args(msg)
        if args is None:
            return

        called_cmd = args[0][len(self.command_startswith):]
        args = args[1:]

        logger.debug('Called command {} with arguments {}'.format(called_cmd, args))
        for cmd in self.__commands:
            if called_cmd == cmd.cmd or called_cmd in cmd.aliases:
                self.queue.put(lambda: cmd.run(msg.thread, msg.author, *args))
                return
        logger.debug('There is no registered command like that')

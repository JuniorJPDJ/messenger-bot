# coding: utf-8
__author__ = 'JuniorJPDJ'

import logging
import sys
import os
import imp
from getpass import getpass
from threading import Thread
from messenger_api.MessengerAPI import Messenger
from messenger_api.MessengerRealTimeChatAPI import MessengerRealTimeChat


class AsyncRun(Thread):
    def __init__(self, what, *args):
        Thread.__init__(self)
        self.what = what
        self.args = args
        self.start()

    def run(self):
        self.what(*self.args)


class MessengerBot(object):
    on = True
    plugin_dir = 'plugins'
    plugins = {}
    groups = []
    # I asked my mate how to call character that starts the string if it is command, he said to call it "Stanisław"
    stanislaw = u"@"
    commands = {}
    cmd_descs = {}

    def __init__(self, messenger, mrtc):
        self.messenger = messenger
        self.mrtc = mrtc
        self.load_plugins()
        mrtc.register_handler('group_msg', self.on_group_msg)

    def add_group(self, group):
        self.groups.append(group)

    def register_command(self, command, handler, desc):
        assert callable(handler)
        if not command.lower() in self.commands:
            self.commands[command.lower()] = handler
            self.cmd_descs[command.lower()] = desc

    def load_plugins(self):
        for i in os.listdir(self.plugin_dir):
            location = os.path.join(self.plugin_dir, i)
            if not (os.path.isdir(location) and "main.py" in os.listdir(location)):
                continue
            path = os.path.abspath(location)
            sys.path.append(path)
            plugin = imp.load_module('main', *imp.find_module('main', [location])).__plugin__
            sys.path.remove(path)
            if plugin.name not in self.plugins:
                self.plugins[plugin.name] = plugin(self)

    def get_plugin(self, name):
        if name in self.plugins:
            return self.plugins[name]

    def on_group_msg(self, datetime, (sender_id, sender_name), (group_id, group_name), message_body, attachments):
        if message_body.find(self.stanislaw) == 0 and len(message_body) != 1 and group_id in self.groups:
            args = ['']
            argnr = 0
            quote_mode = False
            double_quote_mode = False
            escape_mode = False
            for i in message_body:
                if escape_mode:
                    args[argnr] += i
                    escape_mode = False
                elif i == ' ' and not (quote_mode or double_quote_mode):
                    argnr += 1
                    args.append('')
                elif i == "'" and not double_quote_mode:
                    quote_mode = not quote_mode
                elif i == '"' and not quote_mode:
                    double_quote_mode = not double_quote_mode
                elif i == '\\' and not (quote_mode or double_quote_mode):
                    escape_mode = True
                else:
                    args[argnr] += i

            logging.debug(args)

            AsyncRun(self.on_command, sender_name, group_id, args[0][1:], args[1:])

    def on_command(self, sender, thread, command, args):
        if command.lower() in self.commands:
            self.commands[command.lower()](sender, thread, command, args)
        else:
            self.messenger.send_msg(thread, u'Nie ma takiej komendy {}'.format(sender), group=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.info('Logging in')
    if sys.argv[1] and sys.argv[2]:
        email, pw = sys.argv[1:3]
    else:
        email = raw_input('E-mail: ')
        pw = getpass()
    messenger = Messenger(email, pw)
    mrtc = MessengerRealTimeChat(messenger)
    logging.info('Logged in')

    bot = MessengerBot(messenger, mrtc)
    bot.add_group(1403060290008116)
    bot.add_group(1084276031617412)
    bot.add_group(1541353019510339)
    bot.get_plugin('BasePlugin').global_op('Jacek Junior Pruciak')

    for i in bot.groups:
        messenger.send_msg(i, u'[INFO] Bot zalogowany, oczekiwanie na komendy - lista pod komendą @help', group=True)

    while bot.on:
        mrtc.make_pull()

    sys.exit()

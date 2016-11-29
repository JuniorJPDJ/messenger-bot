import logging

from messenger_api.MessengerAPI.Messenger import Messenger
from .PluginLoader import PluginLoader

__author__ = 'JuniorJPDJ'

logger = logging.getLogger(__name__)


class MessengerBot(object):
    def __init__(self, bot_username, bot_password, command_char='.'):
        self.command_char = command_char
        self.msg = Messenger(bot_username, bot_password)

        self.plugin_loader = PluginLoader()
        self.plugin_loader.load_plugins()

        logger.info('Started')

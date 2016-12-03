from .MessengerBot import MessengerBot

__author__ = "JuniorJPDJ"

class Plugin(object):
    name = "override_me"

    def __init__(self, bot):
        assert isinstance(bot, MessengerBot)
        self.bot = bot

from ..Plugin import Plugin

__author__ = 'JuniorJPDJ'


class WelcomeMessagePlugin(Plugin):
    name = 'welcome_message'

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        for t in self.bot.threads:
            t.send_message('Hi, I\'m a bit botish :C')

__plugin__ = WelcomeMessagePlugin

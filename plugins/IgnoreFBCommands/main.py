# coding: utf-8
__author__ = 'Junior'

import logging


class IgnoreFBCommands(object):
    name = "IgnoreFBCommands"

    def __init__(self, bot):
        self.bot = bot
        bot.register_command(u'fbchess', self.nothing, u'szachy fejsboga')
        bot.register_command(u'dailycute', self.nothing, u'spam gównem fejsboga')
        logging.info(u'IgnoreFBCommands loaded')

    @staticmethod
    def nothing(*everything):
        return


__plugin__ = IgnoreFBCommands

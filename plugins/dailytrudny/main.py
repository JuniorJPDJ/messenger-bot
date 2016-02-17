# coding: utf-8
__author__ = 'JuniorJPDJ'

import logging
import random
import io

txtfile = 'plugins/dailytrudny/teksty.txt'

class DailyTrudny(object):
    name = "dailytrudny"

    def __init__(self, bot):
        self.bot = bot
        bot.register_command(u'dailytrudny', self.trudny, u'Jestem Kamil Trudny!')
        logging.info(u'dailytrudny loaded')

    def trudny(self, sender, thread, command, args):
        with io.open(txtfile) as f:
            self.bot.messenger.send_msg(thread, random.choice(f.readlines()).rstrip(), group=True)

__plugin__ = DailyTrudny

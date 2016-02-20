# coding: utf-8
__author__ = 'artur9010'

import logging
import random
import io

class DailyGonciarz(object):
    name = "dailygonciarz"
    txtfile = 'plugins/dailygonciarz/teksty.txt'

    def __init__(self, bot):
        self.bot = bot
        bot.register_command(u'dailygonciarz', self.gonciarz, u'Eszelegeszelekk!')
        logging.info(u'dailygonciarz loaded')

    def gonciarz(self, sender, thread, command, args):
        with io.open(self.txtfile) as f:
            self.bot.messenger.send_msg(thread, random.choice(f.readlines()).rstrip(), group=True)

__plugin__ = DailyGonciarz
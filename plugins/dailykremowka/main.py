# coding: utf-8
__author__ = 'JuniorJPDJ'

import logging
import random
import os
from MessengerCreateAttachmentAPI import MessengerCreateAttachment

txt = [u"Best Juan's Pablo kremówki since 2005!", u"Kremówki just arrived :>",
       u"If you want something to eat - eat kremówka!", u"Kremówka is love <3", u"Want kremówka now? :3",
       u"You has met with a terrible kremówka aren't you? :<", u"Juan Pablo likes kremówki, I think you like it too :]"]

imgurl = 'plugins/dailykremowka/img/'

class DailyKremowka(object):
    name = "dailykremowka"

    def __init__(self, bot):
        self.bot = bot
        self.att = MessengerCreateAttachment(bot.messenger)
        bot.register_command(u'dailykremowka', self.kremowka, u'Janek Paweu Drógi')
        logging.info(u'dailykremówka loaded')

    def kremowka(self, sender, thread, command, args):
        if sender == "Artur Motyka":
            self.bot.messenger.send_msg(thread, u'Nie dam kremówki, wal się grubasie!', group=True)
        else:
            img = self.att.attach_file(imgurl + random.choice(os.listdir(imgurl)))
            self.bot.messenger.send_msg(thread, random.choice(txt), img, True)



__plugin__ = DailyKremowka

# coding: utf-8
__author__ = 'JuniorJPDJ'

import logging
from collections import defaultdict


class BasePlugin(object):
    name = "BasePlugin"

    def __init__(self, bot):
        self.bot = bot
        self._ops = defaultdict(lambda: set())
        self._global_ops = set()
        bot.register_command(u'help', self.command_help, u'wyświetla pomoc')
        bot.register_command(u'ping', self.command_ping, u'odsyła wiadomość pong')
        bot.register_command(u'say', self.command_say, u'wysyła wiadomość')
        bot.register_command(u'ops', self.command_ops, u'wyświetla listę operatorów')
        bot.register_command(u'op', self.command_op, u'dodaje użytkownika do listy operatorów')
        bot.register_command(u'deop', self.command_deop, u'usuwa użytkownika z listy operatorów')
        bot.register_command(u'amiop', self.command_amiop, u'sprawdza czy jesteś operatorem')
        bot.register_command(u'plugins', self.command_plugins, u'wyświetla liste pluginów')
        bot.register_command(u'halt', self.command_halt, u'wyłącza bota')
        bot.register_command(u'kaziciota', self.kaziciota, u'tak')
        logging.info(u'BasePlugin loaded')

    # <op_management>
    def is_op(self, thread, user):
        if user in self._global_ops:
            return True
        elif user in self._ops[thread]:
            return True
        else:
            return False

    def is_global_op(self, user):
        return user in self._global_ops

    def global_op(self, user):
        if not self.is_global_op(user):
            self.global_deop(user)
            self._global_ops.add(user)

    def op(self, thread, user):
        if not self.is_op(thread, user):
            self._ops[thread].add(user)

    def global_deop(self, user):
        if self.is_global_op(user):
            self._global_ops.remove(user)
        else:
            for t in self._ops:
                self.deop(t, user)

    def deop(self, thread, user):
        if user in self._ops[thread]:
            self._ops[thread].remove(user)

    def list_ops(self, thread):
        return self._global_ops.union(self._ops[thread])

    def list_global_ops(self):
        return self._global_ops.copy()
    # </op_management>

    # <commands>
    def command_help(self, sender, thread, command, args):
        out = u'Lista dostępnych komend:\n'
        for c in self.bot.cmd_descs:
            if c != u'kaziciota':
                out += u"{}{} - {}\n".format(self.bot.stanislaw, c, self.bot.cmd_descs[c])
        out += u"##messenger-bot by JuniorJPDJ"
        self.bot.messenger.send_msg(thread, out, group=True)

    def command_ping(self, sender, thread, command, args):
        self.bot.messenger.send_msg(thread, u'PONG! - specialnie dla: {}'.format(sender), group=True)

    def command_say(self, sender, thread, command, args):
        if not self.is_op(thread, sender):
            self.bot.messenger.send_msg(thread, u'Nie masz uprawnień {}'.format(sender), group=True)
        elif len(args) == 0:
            self.bot.messenger.send_msg(thread, u'Podałeś/aś błędną ilość argumentów {}'.format(sender), group=True)
        else:
            txt = u""
            for i in args:
                txt += i + u" "
            self.bot.messenger.send_msg(thread, txt, group=True)

    def command_ops(self, sender, thread, command, args):
        oplist = u''
        for op in self.list_ops(thread):
            oplist += ', ' + op
        self.bot.messenger.send_msg(thread, u'Bot ma nastepujacych operatorów:{}'.format(oplist[1:]), group=True)

    def command_op(self, sender, thread, command, args):
        if self.is_op(thread, sender):
            if len(args) != 1:
                self.bot.messenger.send_msg(thread, u'Podałeś/aś błędną ilość argumentów {}'.format(sender), group=True)
                return
            if self.is_op(thread, args[0]):
                self.bot.messenger.send_msg(thread, u'{} był już operatorem'.format(args[0]), group=True)
                return
            self.op(thread, args[0])
            self.bot.messenger.send_msg(thread, u'{} został(a) operatorem bota!'.format(args[0]), group=True)
        else:
            self.bot.messenger.send_msg(thread, u'Nie masz uprawnień {}'.format(sender), group=True)

    def command_deop(self, sender, thread, command, args):
        if self.is_op(thread, sender):
            if len(args) != 1:
                self.bot.messenger.send_msg(thread, u'Podałeś/aś błędną ilość argumentów {}'.format(sender), group=True)
                return
            if self.is_global_op(args[0]):
                self.bot.messenger.send_msg(thread, u'{} jest operatorem globalnym, nie możesz tego zrobić {}'.format(args[0], sender), group=True)
                return
            self.deop(thread, args[0])
            self.bot.messenger.send_msg(thread, u'{} został(a) pozbawiony/na uprawnień operatora bota!'.format(args[0]), group=True)
        else:
            self.bot.messenger.send_msg(thread, u'Nie masz uprawnień {}'.format(sender), group=True)

    def command_amiop(self, sender, thread, command, args):
        self.bot.messenger.send_msg(thread, u'{} - jesteś operatorem bota :D'.format(sender) if self.is_op(thread, sender) else u'{} - nie jesteś operatorem bota :('.format(sender), group=True)

    def command_plugins(self, sender, thread, command, args):
        out = u''
        for p in self.bot.plugins:
            out += ', ' + p
        self.bot.messenger.send_msg(thread, u'Pluginy zainstalowane w bocie:{}'.format(out[1:]), group=True)

    def command_halt(self, sender, thread, command, args):
        if self.is_global_op(sender):
            for g in self.bot.groups:
                self.bot.messenger.send_msg(g, u'Trwa wyłączanie bota na prośbę {}'.format(sender), group=True)
            self.bot.on = False
        else:
            self.bot.messenger.send_msg(thread, u'Nie masz uprawnień {} (trzeba byc global opem)'.format(sender), group=True)

    def kaziciota(self, sender, thread, command, args):
        self.bot.messenger.send_msg(thread, u"Zdecydowanie tak, wszyscy zgadzamy się z {}, prawda?".format(sender), group=True)
    # </commands>


__plugin__ = BasePlugin
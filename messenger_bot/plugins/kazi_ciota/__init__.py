from ...Plugin import Plugin
from ...Command import Command

__author__ = 'JuniorJPDJ'


class KaziCiotaPlugin(Plugin):
    name = 'kazi_ciota'

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.cmd = KaziCiotaCommand()
        self.bot.register_command(self.cmd)


class KaziCiotaCommand(Command):
    def __init__(self):
        name = "kaziciota"
        desc = "Kazi ciota!"
        aliases = ["kazi_ciota"]
        Command.__init__(self, name, desc, aliases)

    def run(self, thread, sender, *args):
        thread.send_message('Masz racje {}!'.format(sender.short_name))

__plugin__ = KaziCiotaPlugin

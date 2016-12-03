import sys

from ...Plugin import Plugin
from ...Command import Command

if sys.version_info >= (3, 0):
    # noinspection PyUnresolvedReferences
    from urllib.parse import quote_plus
else:
    # noinspection PyUnresolvedReferences
    from urllib import quote_plus


__author__ = 'JuniorJPDJ'


class DuckDuckPlugin(Plugin):
    name = 'duckduckgo'

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.cmd = DuckDuckCommand()
        self.bot.register_command(self.cmd)


class DuckDuckCommand(Command):
    def __init__(self):
        name = ""
        desc = "Replying with duckduckgo.com url"
        aliases = ["ddg", "duckduckgo"]
        Command.__init__(self, name, desc, aliases)

    def run(self, thread, sender, *args):
        query = quote_plus(' '.join(args))
        thread.send_message("Here's your duck {}:\nhttps://duckduckgo.com/?q={}".format(sender.short_name, query))

__plugin__ = DuckDuckPlugin

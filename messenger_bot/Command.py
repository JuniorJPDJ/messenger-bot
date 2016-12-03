__author__ = 'JuniorJPDJ'

class Command(object):
    def __init__(self, cmd, desc, aliases=None):
        """
        :type cmd: str
        :type desc: str
        :type aliases: iterable of str
        """
        self.cmd, self.desc = cmd, desc
        self.aliases = [] if aliases is None else aliases

    def run(self, thread, sender, *args):
        """
        :type thread: Thread
        :type sender: Person
        :rtype str
        """
        raise NotImplementedError()

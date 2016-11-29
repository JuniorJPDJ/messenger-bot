from messenger_api.MessengerAPI.Messenger import Messenger
from PluginLoader import PluginLoader

__author__ = 'JuniorJPDJ'


class MessengerBot(object):
    def __init__(self, bot_username, bot_password):
        self.msg = Messenger(bot_username, bot_password)

        self.plugin_loader = PluginLoader()
        self.plugin_loader.load_plugins()

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description='Messenger Group Bot')
    p.add_argument()

    bot = MessengerBot('frydpol84@poczta.fm', 'q96b63zmknjR')
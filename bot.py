from __future__ import unicode_literals

import logging

from messenger_bot.MessengerBot import MessengerBot


__author__ = 'JuniorJPDJ'

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('login')
    p.add_argument('password')
    p.add_argument('thread_id', type=int, nargs='+', help='messenger thread id')
    p.add_argument('-v', dest='logger_level', action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='verbose mode')
    p.add_argument('-c', dest='cmd_startswith', help='command starting string', default='!')
    p.add_argument('-p', dest='plugin_dir', help='plugin directory', default='plugins')
    args = p.parse_args()

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(name)s: %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        level=args.logger_level)

    bot = MessengerBot(args.login, args.password, args.thread_id, args.cmd_startswith, args.plugin_dir)

    while True:
        bot.pull()

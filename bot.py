import logging

from messenger_bot.MessengerBot import MessengerBot

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('login')
    p.add_argument('password')
    p.add_argument('-v', dest='logger_level', action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='verbose mode')
    args = p.parse_args()

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(name)s: %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        level=args.logger_level)

    bot = MessengerBot(args.login, args.password)

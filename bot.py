from messenger_bot.MessengerBot import MessengerBot

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('login')
    p.add_argument('password')
    args = p.parse_args()

    bot = MessengerBot(args.login, args.password)

#!/usr/bin/env python

from slackbot.bot import Bot
from slacker import Slacker # for sending messages
import schedule
from mybot.plugins import get_statistics
from mybot.plugins import get_daily_statistics
import threading
import time
import os

class ScheduleThread(threading.Thread):
    def __init__(self, *pargs, **kwargs):
        super().__init__(*pargs, daemon=True, name="scheduler", **kwargs)

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(schedule.idle_seconds())

def send_statistics(bot):
    s = 'Daily Notification\n'
    s += 'Total AC:\n'
    s += '\n'.join(get_statistics())
    s += '\n'
    s += get_daily_statistics()
    slacker = Slacker(os.environ['SLACKBOT_API_TOKEN'])
    channel = os.environ['BOT_NOTIFICATION_CHANNEL']
    print('channel:', channel)
    print('message:', s)
    slacker.chat.post_message(channel, s)
    # bot._client.send_message(
            # channel=channel,
            # message=s)

def main():
    bot = Bot()

    schedule.every().sunday.at("22:00").do(send_statistics, bot=bot)
    schedule.every().monday.at("10:00").do(send_statistics, bot=bot)
    schedule.every().tuesday.at("10:00").do(send_statistics, bot=bot)
    schedule.every().wednesday.at("10:00").do(send_statistics, bot=bot)
    schedule.every().thursday.at("10:00").do(send_statistics, bot=bot)
    schedule.every().friday.at("10:00").do(send_statistics, bot=bot)
    schedule.every().saturday.at("22:00").do(send_statistics, bot=bot)

    ScheduleThread().start()


    bot.run()

if __name__ == "__main__":
    main()

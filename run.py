#!/usr/bin/env python

from slackbot.bot import Bot
import schedule
from mybot.plugins import get_statistics
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
    s = 'Weekly Notification\n'
    s += '\n'.join(get_statistics())
    bot._client.rtm_send_message(
            channel=os.environ['BOT_NOTIFICATION_CHANNEL'],
            message=s)

def main():
    bot = Bot()

    schedule.every().friday.at("22:00").do(send_statistics, bot=bot)
    ScheduleThread().start()


    bot.run()

if __name__ == "__main__":
    main()

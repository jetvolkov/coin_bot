import time
import logging
import schedule

from telegram.ext import (
    Filters,
    Updater,
    MessageHandler,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)

from coin.ping import ping
from coin.simple import price

from settings import TOKEN

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text, ping, run_async=True))

logging.info("Start bot.")
updater.start_polling()

schedule.every(10).minutes.do(
    price, ids=["bitcoin", "ethereum"], currencies=["usd", "eur", "rub"]
)

while True:
    schedule.run_pending()
    time.sleep(1)

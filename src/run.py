import time
import logging

from telegram.ext import (
    Filters,
    Updater,
    MessageHandler,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)

from coin.simple import send_price
from settings import TOKEN, UPDATE_TIME
from utils.cmd import Command
from handlers.commands import start
from handlers.callbacks import supported_currencies

updater = Updater(token=TOKEN)
job_queue = updater.job_queue
dispatcher = updater.dispatcher

# dispatcher.add_handler(MessageHandler(Filters.text, ping, run_async=True))

# callbacks
dispatcher.add_handler(
    CallbackQueryHandler(
        supported_currencies,
        pattern=r"^set_currencies$|^next_currencies$|^previous_currencies$",
        run_async=True,
    )
)

# commands
dispatcher.add_handler(CommandHandler(Command.START, start, run_async=True))

logging.info("Start bot.")
updater.start_polling()

job_minute = job_queue.run_repeating(send_price, interval=UPDATE_TIME)

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

from settings import TOKEN, UPDATE_TIME
from utils.cmd import Command
from handlers.commands import start
from handlers.callbacks import supported_currencies

updater = Updater(token=TOKEN)
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

schedule.every(UPDATE_TIME).hours.do(
    supported_currencies
)

while True:
    schedule.run_pending()
    time.sleep(1)

import time
import logging

from telegram.ext import (
    Filters,
    Updater,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from coin.simple import send_price
from settings import TOKEN, UPDATE_TIME
from utils.cmd import Command, Callback
from handlers import commands
from handlers.callbacks import coins, settings, currencies, notifications

updater = Updater(token=TOKEN)
job_queue = updater.job_queue
dispatcher = updater.dispatcher

# callbacks
dispatcher.add_handler(
    CallbackQueryHandler(
        settings.settings,
        pattern=rf"^{Callback.SETTINGS[1]}$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        notifications.show_notification,
        pattern=rf"^{Callback.NOTIFICATION[1]}$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        coins.show_coin_list,
        pattern=rf"^{Callback.COIN_LIST[1]}_\w$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        coins.show_coin_list_menu,
        pattern=rf"^{Callback.COIN_LIST_MENU[1]}$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        coins.manage_coin_list,
        pattern=rf"^{Callback.NEXT_COIN_LIST[1]}$|^{Callback.PREVIOUS_COIN_LIST[1]}$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        coins.coin_settings,
        pattern=rf"^{Callback.COIN_ID}_",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        coins.add_coin_in_notification,
        pattern=rf"^{Callback.ADD_COIN_IN_NOTIFICATION[1]}_",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        currencies.currencies_list,
        pattern=rf"^{Callback.CURRENCIES_LIST[1]}$|^{Callback.NEXT_CURRENCIES[1]}$|^{Callback.PREVIOUS_CURRENCIES[1]}$",
        run_async=True,
    )
)

# commands
dispatcher.add_handler(CommandHandler(Command.START, commands.start, run_async=True))

logging.info("Start bot.")
updater.start_polling()

job_minute = job_queue.run_repeating(send_price, interval=UPDATE_TIME)

updater.idle()

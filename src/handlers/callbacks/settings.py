import logging
from telegram import (
    Update,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from utils.txt import Answer
from utils.cmd import Callback


def settings(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton(
                Callback.COIN_LIST[0], callback_data=Callback.COIN_LIST_MENU[1]
            )
        ],
        [
            InlineKeyboardButton(
                Callback.CURRENCIES_LIST[0], callback_data=Callback.CURRENCIES_LIST[1]
            )
        ],
        [
            InlineKeyboardButton(
                Callback.NOTIFICATION[0], callback_data=Callback.NOTIFICATION[1]
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(
            text="Настройки:", reply_markup=reply_markup
        )
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")

import logging
from httpx import HTTPError
from telegram.ext import CallbackContext
from telegram import (
    Update,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import BadRequest, Unauthorized

from utils.txt import Answer
from utils.cmd import Callback


def show_notification(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton(
                Callback.INTERVAL_NOTIFICATION[0], callback_data=Callback.INTERVAL_NOTIFICATION[1]
            )
        ],
        [
            InlineKeyboardButton(
                Callback.PRICE_NOTIFICATION[0], callback_data=Callback.PRICE_NOTIFICATION[1]
            )
        ],
        [
            InlineKeyboardButton(
                Callback.PERCENT_UP_NOTIFICATION[0], callback_data=Callback.PERCENT_UP_NOTIFICATION[1]
            )
        ],
        [
            InlineKeyboardButton(
                Callback.PERCENT_DOWN_NOTIFICATION[0], callback_data=Callback.PERCENT_DOWN_NOTIFICATION[1]
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(
            text="Выберите тип уведомления:", reply_markup=reply_markup
        )
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")

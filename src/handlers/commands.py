from telegram.ext import CallbackContext
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from utils.cmd import Callback


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(Callback.SET_CURRENCIES[0], callback_data=Callback.SET_CURRENCIES[1])],
    ]

    update.message.reply_text(
        "С чего хотите начать?", reply_markup=InlineKeyboardMarkup(keyboard)
    )

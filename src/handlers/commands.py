import string
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from utils.cmd import Callback


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(Callback.SET_CURRENCIES[0], callback_data=Callback.SET_CURRENCIES[1])],
    ]

    update.message.reply_text(
        "С чего хотите начать?", reply_markup=InlineKeyboardMarkup(keyboard)
    )


def show_coin_list_menu(update: Update, context: CallbackContext):
    keyboard = list()
    inner_keyboard = list()

    add_buttons = [list(), list()]

    for i in range(10):
        add_buttons[0].append(InlineKeyboardButton(str(i), callback_data=f"{Callback.COIN_LIST}_{i}"))

    for i in string.ascii_uppercase:
        add_buttons[1].append(InlineKeyboardButton(i, callback_data=f"{Callback.COIN_LIST}_{i}"))

    add_buttons[1] = [add_buttons[1][x:x + 5] for x in range(0, len(add_buttons[1]), 5)]

    keyboard.append(inner_keyboard)
    keyboard.append(add_buttons[0][0:5])
    keyboard.append(add_buttons[0][5:10])

    for i in add_buttons[1]:
        keyboard.append(i)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        try:
            update.callback_query.message.edit_text(text="Список коинов:", reply_markup=reply_markup)
        except (BadRequest, Unauthorized) as err:
            logging.error(f"{str(err)} {update.effective_user.id}")

    else:
        try:
            update.message.reply_text(text="Список коинов:", reply_markup=reply_markup)
        except (BadRequest, Unauthorized) as err:
            logging.error(f"{str(err)} {update.effective_user.id}")

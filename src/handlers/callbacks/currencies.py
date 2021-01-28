import logging
import itertools
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
from coin.simple import supported_currencies


def currencies_list(update: Update, context: CallbackContext):
    callback_query = update.callback_query.data
    add_buttons = [
        InlineKeyboardButton(
            Callback.PREVIOUS_CURRENCIES[0],
            callback_data=Callback.PREVIOUS_CURRENCIES[1],
        ),
        InlineKeyboardButton(
            Callback.NEXT_CURRENCIES[0], callback_data=Callback.NEXT_CURRENCIES[1]
        ),
    ]

    if callback_query == Callback.NEXT_CURRENCIES[1]:
        currencies = context.user_data["currencies_list"]
        idx = context.user_data["currencies_list_index"]
        pidx = idx + 1
        nidx = idx + 11

    elif callback_query == Callback.PREVIOUS_CURRENCIES[1]:
        currencies = context.user_data["currencies_list"]
        idx = context.user_data["currencies_list_index"]
        k = idx % 10 if idx == len(currencies) - 1 else 9
        pidx = idx - (10 + k)
        nidx = idx - k

        if pidx == 0:
            del add_buttons[0]

    else:
        pidx = 0
        nidx = 10
        currencies = supported_currencies()
        context.user_data["currencies_list"] = currencies
        del add_buttons[0]

    keyboard = list()
    inner_keyboards = list()

    for currency in itertools.islice(currencies, pidx, nidx):
        inner_keyboards.append(
            InlineKeyboardButton(currency.upper(), callback_data=currency)
        )
        context.user_data["currencies_list_index"] = currencies.index(currency)

    if context.user_data["currencies_list_index"] == len(currencies) - 1:
        del add_buttons[1]

    for inner_keyboard in inner_keyboards:
        keyboard.append([inner_keyboard])

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.edit_message_text(
            text=Answer.SELECT_CURRENCY, reply_markup=reply_markup
        )
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")

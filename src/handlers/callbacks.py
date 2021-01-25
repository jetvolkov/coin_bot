import logging
from telegram.ext import CallbackContext
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import BadRequest, Unauthorized

from utils.cmd import Callback
from coin.simple import supported_currencies


# TODO сделать так чтобы функция работала правильно
def supported_currencies(
    update: Update, context: CallbackContext
):
    callback_query = update.callback_query.data
    txt = "Выберите валюту для перевода(можно выбрать несколько)."

    next_button = InlineKeyboardButton(
        Callback.NEXT_CURRENCIES[0], callback_data=Callback.NEXT_CURRENCIES[1]
    )
    previous_button = InlineKeyboardButton(
        Callback.PREVIOUS_CURRENCIES[0], callback_data=Callback.PREVIOUS_CURRENCIES[1]
    )

    if callback_query == Callback.NEXT_CURRENCIES[1]:
        currencies = context.user_data["supported_currencies"]
        last_currency = context.user_data["last_currency"]
        start_currencies = currencies.index(last_currency) + 1

        if start_currencies + 15 >= len(currencies):
            add_buttons = [previous_button]
        else:
            add_buttons = [previous_button, next_button]

    elif callback_query == Callback.PREVIOUS_CURRENCIES[1]:
        currencies = context.user_data["supported_currencies"]
        last_currency = context.user_data["last_currency"]
        start_currencies = currencies.index(last_currency)

        if start_currencies == 0:
            add_buttons = [next_button]
        else:
            add_buttons = [previous_button, next_button]

    else:
        start_currencies = 0
        currencies = supported_currencies()
        context.user_data["supported_currencies"] = currencies
        add_buttons = [next_button]

    keyboard = list()
    tmp_list = list()

    logging.info(start_currencies)

    for idx, currency in enumerate(currencies[start_currencies:], start=1):
        context.user_data["last_currency"] = currency

        tmp_list.append(InlineKeyboardButton(currency.upper(), callback_data=currency))

        if len(tmp_list) == 5 or len(currencies) == currencies.index(currency):
            keyboard.append(tmp_list)
            tmp_list = list()

        if idx == 15:
            keyboard.append(tmp_list)
            break

    logging.info(context.user_data["last_currency"])
    logging.info(currencies.index(context.user_data["last_currency"]))

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.edit_message_text(txt, reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")

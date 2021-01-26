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
from coin.coins import coin_list as cl, info
from coin.simple import supported_currencies


# TODO сделать так чтобы функция работала правильно
def supported_currencies(update: Update, context: CallbackContext):
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
    inner_keyboard = list()

    logging.info(start_currencies)

    for idx, currency in enumerate(currencies[start_currencies:], start=1):
        context.user_data["last_currency"] = currency

        inner_keyboard.append(
            InlineKeyboardButton(currency.upper(), callback_data=currency)
        )

        if len(inner_keyboard) == 5 or len(currencies) == currencies.index(currency):
            keyboard.append(inner_keyboard)
            inner_keyboard = list()

        if idx == 15:
            keyboard.append(inner_keyboard)
            break

    logging.info(context.user_data["last_currency"])
    logging.info(currencies.index(context.user_data["last_currency"]))

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.edit_message_text(txt, reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def show_coin_list(update: Update, context: CallbackContext):
    try:
        coins = cl()
    except HTTPError as err:
        update.message.reply_text(Answer.SERVER_ERROR)
        logging.error(str(err))
        return

    callback_data = update.callback_query.data.replace("coin_list_", "")
    coins = [coin for coin in coins if coin["name"].startswith(callback_data)]
    context.user_data["coin_list"] = coins

    keyboard = list()
    add_buttons = list()
    inner_keyboards = list()

    add_buttons.append(
        InlineKeyboardButton(
            Callback.COIN_LIST_MENU[0], callback_data=Callback.COIN_LIST_MENU[1]
        )
    )
    add_buttons.append(
        InlineKeyboardButton(
            Callback.NEXT_COIN_LIST[0], callback_data=Callback.NEXT_COIN_LIST[1]
        )
    )

    for coin in itertools.islice(coins, 10):
        inner_keyboards.append(
            InlineKeyboardButton(coin["name"], callback_data=f"coin_id_{coin['id']}")
        )
        context.user_data["coin_list_index"] = coins.index(coin)

    for inner_keyboard in inner_keyboards:
        keyboard.append([inner_keyboard])

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(text="Список коинов:", reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def manage_coin_list(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data
    coins = context.user_data["coin_list"]

    keyboard = list()
    add_buttons = list()
    inner_keyboards = list()

    add_buttons.append(
        InlineKeyboardButton(
            Callback.COIN_LIST_MENU[0], callback_data=Callback.COIN_LIST_MENU[1]
        )
    )
    add_buttons.append(
        InlineKeyboardButton(
            Callback.PREVIOUS_COIN_LIST[0], callback_data=Callback.PREVIOUS_COIN_LIST[1]
        )
    )
    add_buttons.append(
        InlineKeyboardButton(
            Callback.NEXT_COIN_LIST[0], callback_data=Callback.NEXT_COIN_LIST[1]
        )
    )

    logging.warning("start" + str(context.user_data["coin_list_index"]))

    if callback_data == Callback.NEXT_COIN_LIST[1]:
        idx = context.user_data["coin_list_index"]
        for coin in itertools.islice(coins, idx + 1, idx + 11):
            inner_keyboards.append(
                InlineKeyboardButton(coin["name"], callback_data=f"coin_id_{coin['id']}")
            )
            context.user_data["coin_list_index"] = coins.index(coin)

        if context.user_data["coin_list_index"] == len(coins) - 1:
            del add_buttons[2]

    else:
        idx = context.user_data["coin_list_index"]
        k = idx % 10 if context.user_data["coin_list_index"] == len(coins) - 1 else 9
        pidx = idx - (10 + k)

        for coin in itertools.islice(coins, pidx, idx - k):
            inner_keyboards.append(
                InlineKeyboardButton(coin["name"], callback_data=f"coin_id_{coin['id']}")
            )
            context.user_data["coin_list_index"] = coins.index(coin)

        if pidx == 0:
            del add_buttons[1]

    logging.warning("end" + str(context.user_data["coin_list_index"]))

    for inner_keyboard in inner_keyboards:
        keyboard.append([inner_keyboard])

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_reply_markup(reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def coin_settings(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data.replace("coin_id_", "")
    coin = info(callback_data)

    txt = f"id: {coin['id']}\n" \
          f"Имя: {coin['name']}\n" \
          f"Условное обозначение: {coin['symbol']}\n" \
          f"Дата возникновения: {coin['genesis_date']}\n" \
          f"Описание: {coin['description']['en']}"

    keyboard = list()
    add_buttons = [
        InlineKeyboardButton(
            Callback.COIN_LIST_MENU[0], callback_data=Callback.COIN_LIST_MENU[1]
        ),
        InlineKeyboardButton(
            Callback.ADD_IN_NOTIFICATION[0], callback_data=Callback.ADD_IN_NOTIFICATION[1]
        )
    ]

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(text=txt, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def add_in_notification(update: Update, context: CallbackContext):
    pass

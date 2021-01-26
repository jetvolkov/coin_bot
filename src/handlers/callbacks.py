import string
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


def settings(update: Update, context: CallbackContext):
    keyboard = list()
    add_buttons = [
        InlineKeyboardButton(
            Callback.COIN_LIST[0], callback_data=Callback.COIN_LIST_MENU[1]
        ),
        InlineKeyboardButton(
            Callback.CURRENCIES_LIST[0], callback_data=Callback.CURRENCIES_LIST[1]
        )
    ]

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(text="Настройки:", reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


# TODO сделать так чтобы функция работала правильно
def currencies_list(update: Update, context: CallbackContext):
    callback_query = update.callback_query.data
    add_buttons = [
        InlineKeyboardButton(
            Callback.PREVIOUS_CURRENCIES[0], callback_data=Callback.PREVIOUS_CURRENCIES[1]
        ),
        InlineKeyboardButton(
            Callback.NEXT_CURRENCIES[0], callback_data=Callback.NEXT_CURRENCIES[1]
        )
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
        update.callback_query.edit_message_text(text=Answer.SELECT_CURRENCY, reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def show_coin_list_menu(update: Update, context: CallbackContext):
    keyboard = list()
    inner_keyboard = list()

    add_buttons = [list(), list()]

    for i in range(10):
        add_buttons[0].append(InlineKeyboardButton(str(i), callback_data=f"{Callback.COIN_LIST[1]}_{i}"))

    for i in string.ascii_uppercase:
        add_buttons[1].append(InlineKeyboardButton(i, callback_data=f"{Callback.COIN_LIST[1]}_{i}"))

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
    if len(coins) >= 10:
        add_buttons.append(
            InlineKeyboardButton(
                Callback.NEXT_COIN_LIST[0], callback_data=Callback.NEXT_COIN_LIST[1]
            )
        )

    for coin in itertools.islice(coins, 10):
        inner_keyboards.append(
            InlineKeyboardButton(coin["name"], callback_data=f"{Callback.COIN_ID}_{coin['id']}")
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
    inner_keyboards = list()
    add_buttons = [
        InlineKeyboardButton(
            Callback.COIN_LIST_MENU[0], callback_data=Callback.COIN_LIST_MENU[1]
        ),
        InlineKeyboardButton(
            Callback.PREVIOUS_COIN_LIST[0], callback_data=Callback.PREVIOUS_COIN_LIST[1]
        ),
        InlineKeyboardButton(
            Callback.NEXT_COIN_LIST[0], callback_data=Callback.NEXT_COIN_LIST[1]
        )
    ]

    if callback_data == Callback.NEXT_COIN_LIST[1]:
        idx = context.user_data["coin_list_index"]
        pidx = idx + 1
        nidx = idx + 11

    else:
        idx = context.user_data["coin_list_index"]
        k = idx % 10 if idx == len(coins) - 1 else 9
        pidx = idx - (10 + k)
        nidx = idx - k

        if pidx == 0:
            del add_buttons[1]

    for coin in itertools.islice(coins, pidx, nidx):
        inner_keyboards.append(
            InlineKeyboardButton(coin["name"], callback_data=f"{Callback.COIN_ID}_{coin['id']}")
        )
        context.user_data["coin_list_index"] = coins.index(coin)

    if context.user_data["coin_list_index"] == len(coins) - 1:
        del add_buttons[2]

    for inner_keyboard in inner_keyboards:
        keyboard.append([inner_keyboard])

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_reply_markup(reply_markup=reply_markup)
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def coin_settings(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data.replace(f"{Callback.COIN_ID}_", "")
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

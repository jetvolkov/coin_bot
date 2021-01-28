import string
import logging
import itertools
from httpx import HTTPError
from telegram import (
    Update,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from peewee import IntegrityError
from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from settings import db
from utils.txt import Answer
from utils.cmd import Callback
from models import Coin, Person
from coin.coins import coin_list as cl, info


def show_coin_list_menu(update: Update, context: CallbackContext):
    keyboard = list()
    inner_keyboard = list()

    add_buttons = [list(), list()]

    for i in range(10):
        add_buttons[0].append(
            InlineKeyboardButton(str(i), callback_data=f"{Callback.COIN_LIST[1]}_{i}")
        )

    for i in string.ascii_uppercase:
        add_buttons[1].append(
            InlineKeyboardButton(i, callback_data=f"{Callback.COIN_LIST[1]}_{i}")
        )

    add_buttons[1] = [
        add_buttons[1][x: x + 5] for x in range(0, len(add_buttons[1]), 5)
    ]

    keyboard.append(inner_keyboard)
    keyboard.append(add_buttons[0][0:5])
    keyboard.append(add_buttons[0][5:10])

    for i in add_buttons[1]:
        keyboard.append(i)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        try:
            update.callback_query.message.edit_text(
                text="Список коинов:", reply_markup=reply_markup
            )
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
            InlineKeyboardButton(
                coin["name"], callback_data=f"{Callback.COIN_ID}_{coin['id']}"
            )
        )
        context.user_data["coin_list_index"] = coins.index(coin)

    for inner_keyboard in inner_keyboards:
        keyboard.append([inner_keyboard])

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(
            text="Список коинов:", reply_markup=reply_markup
        )
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
        ),
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
            InlineKeyboardButton(
                coin["name"], callback_data=f"{Callback.COIN_ID}_{coin['id']}"
            )
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

    txt = (
        f"id: {coin['id']}\n"
        f"Имя: {coin['name']}\n"
        f"Условное обозначение: {coin['symbol']}\n"
        f"Дата возникновения: {coin['genesis_date']}\n"
        f"Описание: {coin['description']['en']}"
    )

    keyboard = list()
    add_buttons = [
        InlineKeyboardButton(
            Callback.COIN_LIST_MENU[0], callback_data=Callback.COIN_LIST_MENU[1]
        ),
        InlineKeyboardButton(
            Callback.ADD_COIN_IN_NOTIFICATION[0],
            callback_data=f"{Callback.ADD_COIN_IN_NOTIFICATION[1]}_{coin['id']}",
        ),
    ]

    keyboard.append(add_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.edit_text(
            text=txt, reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")


def add_coin_in_notification(update: Update, context: CallbackContext):
    coin_id = update.callback_query.data.replace(f"{Callback.ADD_COIN_IN_NOTIFICATION[1]}_", "")
    user_id = update.effective_user.id
    try:
        with db.atomic():
            coin = Coin.create(coin_id=coin_id, person=Person.get(Person.telegram_id == user_id))

        logging.info(coin)
    except IntegrityError as err:
        logging.error(f"{str(err)} {update.effective_user.id}")

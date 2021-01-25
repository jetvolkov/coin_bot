import httpx
import logging
from babel import numbers

from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import BadRequest, Unauthorized

from utils.txt import Answer
from settings import TOKEN, COIN_API, USERS_LIST

bot = Bot(TOKEN)
PRICE_URL = "simple/price"
SUPPORTED_CURRENCIES = "simple/supported_vs_currencies"


def price(ids: list, currencies: list) -> dict:
    url = COIN_API + PRICE_URL
    params = {
        "ids": ",".join(ids),
        "vs_currencies": ",".join(currencies),
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true",
    }
    response = httpx.get(url, params=params)
    return response.json()

    txt = str()
    for coin in data:
        txt += "Курс " + coin.upper() + ":\n"
        for currency in currencies:
            pr = numbers.format_currency(
                data[coin][currency],
                currency.upper(),
                locale="ru_RU",
            )
            txt += f"{currency.upper()}: {pr}\n"

        txt += "\n"

    for chat_id in USERS_LIST:
        try:
            bot.send_message(chat_id, txt)
        except (BadRequest, Unauthorized) as err:
            logging.error(f"{str(err)} {chat_id}")


def supported_currencies() -> list:
    url = COIN_API + SUPPORTED_CURRENCIES
    response = httpx.get(url)
    return response.json()

import httpx
import logging
from babel import numbers

from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from settings import COIN_API, USERS_LIST

PRICE = "simple/price"
SUPPORTED_CURRENCIES = "simple/supported_vs_currencies"


def price(ids: list, currencies: list) -> dict:
    url = COIN_API + PRICE
    params = {
        "ids": ",".join(ids),
        "vs_currencies": ",".join(currencies),
        "include_market_cap": True,
        "include_24hr_vol": True,
        "include_24hr_change": True,
        "include_last_updated_at": True,
    }
    response = httpx.get(url, params=params)
    return response.json()


def supported_currencies() -> list:
    url = COIN_API + SUPPORTED_CURRENCIES
    response = httpx.get(url)
    return response.json()


def send_price(context: CallbackContext):
    coins = price(["bitcoin", "ethereum"], ["usd", "eur", "rub"])
    txt = str()
    for coin in coins:
        txt += "Курс " + coin.upper() + ":\n"
        for currency in ["usd", "eur", "rub"]:
            pr = numbers.format_currency(
                coins[coin][currency],
                currency.upper(),
                locale="ru_RU",
            )
            txt += f"{currency.upper()}: {pr}\n"

        txt += "\n"

    for chat_id in USERS_LIST:
        try:
            context.bot.send_message(chat_id=chat_id, text=txt)
        except (BadRequest, Unauthorized) as err:
            logging.error(f"{str(err)} {chat_id}")

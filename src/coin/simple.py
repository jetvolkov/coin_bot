import httpx
import logging
from babel import numbers

from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from settings import db, COIN_API
from models import Coin, Person
from peewee import JOIN, IntegrityError

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
    try:
        with db.atomic():
            user_list = Person.select()
            logging.warning(user_list)

        for user in user_list:
            coins_price = price([coin.coin_id for coin in user.coins], ["usd", "eur", "rub"])
            txt = str()
            for coin in coins_price:
                txt += "Курс " + coin.upper() + ":\n"
                for currency in ["usd", "eur", "rub"]:
                    pr = numbers.format_currency(
                        coins_price[coin][currency],
                        currency.upper(),
                        locale="ru_RU",
                    )
                    txt += f"{currency.upper()}: {pr}\n"

                txt += "\n"

            logging.info(user)
            try:
                context.bot.send_message(chat_id=user.telegram_id, text=txt)
            except (BadRequest, Unauthorized) as err:
                logging.error(f"{str(err)} {user.telegram_id}")

    except IntegrityError as err:
        logging.error(str(err))




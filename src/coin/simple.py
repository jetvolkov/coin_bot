import httpx
import logging
from telegram import Bot
from telegram.error import BadRequest, Unauthorized

from utils.txt import Answer
from settings import TOKEN, COIN_API, USERS_LIST

bot = Bot(TOKEN)
PRICE_URL = "simple/price"


def price(ids: list, currencies: list):
    url = COIN_API + PRICE_URL
    params = {
        "ids": ",".join(ids),
        "vs_currencies": ",".join(currencies),
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    response = httpx.get(url, params=params)
    data = response.json()

    txt = Answer.MAILING

    for i in data:
        txt += i + "\n"
        for currency in currencies:
            txt += f"\t{currency}: {str(data[i][currency])}\n"

    for chat_id in USERS_LIST:
        try:
            bot.send_message(chat_id, txt)
        except (BadRequest, Unauthorized) as err:
            logging.error(f"{str(err)} {chat_id}")

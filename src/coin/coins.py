import httpx
import logging
from babel import numbers

from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from settings import COIN_API, USERS_LIST

LIST = "coins/list"
INFO = "coins/{}"
TICKERS = "coins/{}/tickers"
HISTORY = "coins/{}/history"



def coin_list() -> list:
    url = COIN_API + LIST
    response = httpx.get(url)
    return response.json()


def info(coin_id: str) -> dict:
    url = COIN_API + INFO.format(coin_id)
    params = {
        "localization": True,
        "market_data": False,
        "community_data": False,
        "developer_data": False,
        "sparkline": False,
    }
    response = httpx.get(url, params=params)
    return response.json()


def tickers(coin_id: str) -> dict:
    url = COIN_API + TICKERS.format(coin_id)
    response = httpx.get(url)
    return response.json()


def history(coin_id: str, date: str) -> dict:
    url = COIN_API + HISTORY.format(coin_id)
    params = {
        "date": date,
        "localization": False,
    }
    response = httpx.get(url, params=params)
    return response.json()

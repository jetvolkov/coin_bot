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


def notification(update: Update, context: CallbackContext):
    data = context.user_data["status"]
    logging.info(data)
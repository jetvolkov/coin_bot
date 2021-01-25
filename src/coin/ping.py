import httpx
from settings import COIN_API

from telegram.ext import CallbackContext
from telegram import Update

from utils.txt import Answer


def ping(update: Update, context: CallbackContext):
    r = httpx.get(COIN_API + "ping")
    if r.is_error:
        update.message.reply_markdown(text=Answer.SERVER_ERROR)
    else:
        ans = r.json()
        update.message.reply_markdown(text=ans["gecko_says"])

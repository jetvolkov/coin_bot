import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from peewee import IntegrityError
from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized

from settings import db
from models import Person
from utils.cmd import Callback


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(Callback.SETTINGS[0], callback_data=Callback.SETTINGS[1])],
    ]

    try:
        update.message.reply_text(
            "С чего хотите начать?", reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except (BadRequest, Unauthorized) as err:
        logging.error(f"{str(err)} {update.effective_user.id}")

    try:
        with db.atomic():
            person = Person.create(
                telegram_id=update.effective_user.id,
                full_name=update.effective_user.full_name,
                language="ru"
            )
        logging.info(person)
    except IntegrityError as err:
        logging.error(f"{str(err)} {update.effective_user.id}")
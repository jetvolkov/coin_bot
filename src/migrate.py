import logging

from models import Coin, Person
from settings import db

if not db.table_exists(Person):
    with db:
        db.create_tables([Coin, Person])

else:
    with db:
        db.drop_tables([Coin, Person])
        db.create_tables([Coin, Person])

logging.info("The tables in the database have been created.")
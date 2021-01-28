from peewee import *
from datetime import datetime


from settings import db


class BaseModel(Model):
    # TODO: переделать поля, сделать auto_now
    create_at = DateTimeField(default=datetime.now)
    update_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Person(BaseModel):
    telegram_id = IntegerField(unique=True)
    full_name = CharField()
    language = CharField()
    interval_notification = CharField(null=True)
    price_notification = CharField(null=True)
    input_price_notification = CharField(null=True)
    input_price_notification_way = CharField(null=True)

    percent_up_notification = CharField(null=True)
    input_percent_up_notification = CharField(null=True)

    percent_down_notification = CharField(null=True)
    input_percent_down_notification = CharField(null=True)

    class Meta:
        table_name = "persons"


class Coin(BaseModel):
    coin_id = CharField()
    person = ForeignKeyField(model=Person, backref="coins", on_delete="CASCADE")

    class Meta:
        table_name = "coins"
        primary_key = CompositeKey("coin_id", "person")

import logging
from environs import Env
from playhouse.postgres_ext import PostgresqlExtDatabase

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    level=logging.INFO,
)

env = Env()
env.read_env()

TOKEN = env.str("TELEGRAM_TOKEN")
COIN_API = "https://api.coingecko.com/api/v3/"

# time in seconds
UPDATE_TIME = env.int("UPDATE_TIME")

# database
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST", "db")
DB_PORT = env.int("DB_PORT", 5432)

db = PostgresqlExtDatabase(
    database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
)

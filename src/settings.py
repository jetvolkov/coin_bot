import logging
from environs import Env

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    level=logging.INFO,
)

env = Env()
env.read_env("../bot.env")

TOKEN = env.str("TELEGRAM_TOKEN")
COIN_API = "https://api.coingecko.com/api/v3/"

USERS_LIST = ["427927822"]

# time in seconds
UPDATE_TIME = 28_800

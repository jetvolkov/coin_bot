class Command:
    HELP = "help"
    START = "start"


class Callback:
    SETTINGS = ["Настройки", "settings"]

    CURRENCIES_LIST = ["Список валют", "currencies_list"]
    NEXT_CURRENCIES = ["Вперед", "next_currencies"]
    PREVIOUS_CURRENCIES = ["Назад", "previous_currencies"]

    COIN_ID = "coin_id"
    COIN_LIST = ["Список криптовалют", "coin_list"]
    COIN_LIST_MENU = ["В меню", "coin_list_menu"]
    NEXT_COIN_LIST = ["Вперед", "next_coin_list"]
    PREVIOUS_COIN_LIST = ["Назад", "previous_coin_list"]

    NOTIFICATION = ["Оповещения", "notification"]
    ADD_COIN_IN_NOTIFICATION = ["В список оповещения", "add_coin_in_notification"]

    # TODO реализовать возможность убирать из списко оповещений
    REMOVE_COIN_IN_NOTIFICATION = ["В список оповещения", "add_coin_in_notification"]

    ADD_CURRENCY_IN_NOTIFICATION = ["В список оповещения", "add_currency_in_notification"]
    INTERVAL_NOTIFICATION = ["Задать интервал", "notification"]
    PRICE_NOTIFICATION = ["Уведомление по цене", "price_notification"]
    PERCENT_UP_NOTIFICATION = ["Уведомление по процентам вверх", "percent_up_notification"]
    PERCENT_DOWN_NOTIFICATION = ["Уведомление по процентам вниз", "percent_down_notification"]
    INPUT_PRICE_NOTIFICATION = ["Ввести стоимость", "input_price_notification"]
    INPUT_PERCENT_UP_NOTIFICATION = ["Ввести проценты", "input_percent_up_notification"]
    INPUT_PERCENT_DOWN_NOTIFICATION = ["Ввести проценты", "input_percent_down_notification"]
    CURRENT_PRICE_NOTIFICATION = ["Использовать текущую стоимость", "current_price_notification"]

class Command:
    HELP = "help"
    LIST = "list"
    START = "start"


class Callback:
    SET_CURRENCIES = ["Выбрать валюту для отображения", "set_currencies"]
    NEXT_CURRENCIES = ["Вперед", "next_currencies"]
    PREVIOUS_CURRENCIES = ["Назад", "previous_currencies"]

    COIN_LIST = "coin_list"
    COIN_LIST_MENU = ["В меню", "coin_list_menu"]
    NEXT_COIN_LIST = ["Вперед", "next_coin_list"]
    PREVIOUS_COIN_LIST = ["Назад", "previous_coin_list"]

    ADD_IN_NOTIFICATION = ["Добавить в список оповещений", "add_in_notification"]

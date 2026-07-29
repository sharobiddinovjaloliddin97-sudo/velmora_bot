from telegram import ReplyKeyboardMarkup

from utils.texts import TEXTS


def get_cart_keyboard(language: str):
    keyboard = [
        [TEXTS[language]["place_order"]],
        [TEXTS[language]["clear_cart"]],
        [TEXTS[language]["catalog"]],
        [TEXTS[language]["main_menu"]],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
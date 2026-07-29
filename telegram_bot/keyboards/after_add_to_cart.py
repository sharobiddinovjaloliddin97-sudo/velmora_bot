from telegram import ReplyKeyboardMarkup

from utils.texts import TEXTS


def get_after_add_to_cart_keyboard(language: str):
    keyboard = [
        [TEXTS[language]["cart"]],
        [TEXTS[language]["categories"]],
        [TEXTS[language]["main_menu"]],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
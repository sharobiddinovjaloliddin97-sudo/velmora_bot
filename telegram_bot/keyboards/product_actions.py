from telegram import ReplyKeyboardMarkup

from utils.texts import TEXTS


def get_product_actions_keyboard(language: str):
    keyboard = [
        [TEXTS[language]["add_to_cart"]],
        [TEXTS[language]["back"]],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
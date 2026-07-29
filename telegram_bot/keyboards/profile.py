from telegram import ReplyKeyboardMarkup
from utils.texts import TEXTS


def get_profile_keyboard(language: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            TEXTS[language]["my_orders"],
        ],
        [
            TEXTS[language]["main_menu"],
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

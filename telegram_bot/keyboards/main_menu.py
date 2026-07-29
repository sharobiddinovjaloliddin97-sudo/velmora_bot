from telegram import ReplyKeyboardMarkup

from utils.texts import TEXTS


def get_main_menu(language: str = "uz"):
    keyboard = [
        [TEXTS[language]["catalog"]],
        [
            TEXTS[language]["cart"],
            TEXTS[language]["profile"],
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

from telegram import ReplyKeyboardMarkup


def get_language_keyboard():
    keyboard = [
        ["🇺🇿 O'zbek"],
        ["🇷🇺 Русский"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
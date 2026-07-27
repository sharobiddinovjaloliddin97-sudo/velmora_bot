from telegram import ReplyKeyboardMarkup

from services.catalog_service import get_categories


def get_catalog_keyboard():
    keyboard = []

    for category in get_categories():
        keyboard.append([category])

    keyboard.append(["🔙 Back"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )


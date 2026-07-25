from telegram import ReplyKeyboardMarkup


def get_main_menu():
    keyboard = [
        ["🛍 Catalog"],
        ["🛒 Cart", "👤 Profile"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
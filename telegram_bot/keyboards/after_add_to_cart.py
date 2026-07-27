from telegram import ReplyKeyboardMarkup


def get_after_add_to_cart_keyboard():
    keyboard = [
        ["🛒 Cart"],
        ["🔙 Products"],
        ["🏠 Main Menu"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
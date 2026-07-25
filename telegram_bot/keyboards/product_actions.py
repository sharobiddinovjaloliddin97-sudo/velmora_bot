from telegram import ReplyKeyboardMarkup


def get_product_actions_keyboard():
    keyboard = [
        ["🛒 Add to Cart"],
        ["🔙 Products"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
from telegram import ReplyKeyboardMarkup


def get_product_keyboard(products):
    keyboard = []

    for product in products:
        keyboard.append([product])

    keyboard.append(["🔙 Categories"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


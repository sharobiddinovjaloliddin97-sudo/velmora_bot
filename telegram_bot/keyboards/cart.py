from telegram import ReplyKeyboardMarkup


def get_cart_keyboard():
    keyboard = [
        ["✅ Place Order"],
        ["🗑 Clear Cart"],
        ["🔙 Back"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
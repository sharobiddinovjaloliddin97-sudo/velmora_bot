from telegram import ReplyKeyboardMarkup

from utils.texts import TEXTS


def get_product_keyboard(products, language="uz"):
    keyboard = []

    for product in products:
        keyboard.append([product["name_uz"] if language == "uz" else product["name_ru"]])

    keyboard.append([TEXTS[language]["categories"]])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
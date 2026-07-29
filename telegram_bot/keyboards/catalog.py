from telegram import ReplyKeyboardMarkup

from services.catalog_service import get_categories
from utils.texts import TEXTS


async def get_catalog_keyboard(language: str = "uz"):
    categories = await get_categories()
    print(categories)

    keyboard = []

    for category in categories:
        if language == "uz":
            keyboard.append([category["name_uz"]])
        else:
            keyboard.append([category["name_ru"]])

    keyboard.append([TEXTS[language]["back"]])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards.catalog import get_catalog_keyboard
from keyboards.main_menu import get_main_menu
from keyboards.product import get_product_keyboard

from services.catalog_service import get_categories
from services.product_service import ProductService

from states import States
from utils.texts import TEXTS


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")
    text = update.message.text

    categories = await get_categories()

    category_map = {}

    for category in categories:
        if language == "uz":
            category_map[category["name_uz"]] = category
        else:
            category_map[category["name_ru"]] = category

    # User pressed Catalog
    if text == TEXTS[language]["catalog"]:
        await update.message.reply_text(
            text=TEXTS[language]["choose_category"],
            reply_markup=await get_catalog_keyboard(language),
        )
        return States.CHOOSING_CATEGORY

    # User selected a category
    if text in category_map:
        selected_category = category_map[text]

        products = await ProductService.get_products(
            selected_category["id"]
        )

        context.user_data["products"] = products

        await update.message.reply_text(
            text=TEXTS[language]["choose_product"].format(
                category=text,
            ),
            reply_markup=get_product_keyboard(
                products,
                language,
            ),
        )

        return States.CHOOSING_PRODUCT

    # Back to categories
    if text == TEXTS[language]["categories"]:
        await update.message.reply_text(
            text=TEXTS[language]["choose_category"],
            reply_markup=await get_catalog_keyboard(language),
        )

        return States.CHOOSING_CATEGORY

    # Back to main menu
    if text == TEXTS[language]["back"]:
        await update.message.reply_text(
            text=TEXTS[language]["main_menu"],
            reply_markup=get_main_menu(language),
        )

        return ConversationHandler.END

    return States.CHOOSING_CATEGORY
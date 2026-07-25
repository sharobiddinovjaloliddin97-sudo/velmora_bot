from telegram import Update
from telegram.ext import ContextTypes

from keyboards.catalog import get_catalog_keyboard
from keyboards.main_menu import get_main_menu
from keyboards.product import get_product_keyboard

from services.catalog_service import get_categories
from services.product_service import ProductService


categories = {
    category: category.replace("🍕 ", "").replace("🍔 ", "").replace("🥤 ", "")
    for category in get_categories()
}


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🛍 Catalog":
        await update.message.reply_text(
            text="📦 Choose a category:",
            reply_markup=get_catalog_keyboard(),
        )

    elif text in categories:
        category = categories[text]

        products = await ProductService.get_products(category)

        await update.message.reply_text(
            text=f"📦 {category}\n\nChoose a product:",
            reply_markup=get_product_keyboard(products),
        )

    elif text == "🔙 Categories":
        await update.message.reply_text(
            text="📦 Choose a category:",
            reply_markup=get_catalog_keyboard(),
        )

    elif text == "🔙 Back":
        await update.message.reply_text(
            text="🏠 Main Menu",
            reply_markup=get_main_menu(),
        )


        
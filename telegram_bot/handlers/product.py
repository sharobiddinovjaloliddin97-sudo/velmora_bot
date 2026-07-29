from telegram import Update
from telegram.ext import ContextTypes

from keyboards.product import get_product_keyboard
from keyboards.product_actions import get_product_actions_keyboard

from states import States
from utils.texts import TEXTS


async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")
    text = update.message.text

    # ===========================
    # Back to product list
    # ===========================
    if text == TEXTS[language]["back"]:
        products = context.user_data.get("products", [])

        await update.message.reply_text(
            text=TEXTS[language]["choose_product"],
            reply_markup=get_product_keyboard(
                products,
                language,
            ),
        )

        return States.CHOOSING_PRODUCT

    # ===========================
    # Find selected product
    # ===========================
    products = context.user_data.get("products", [])

    product = next(
        (
            p for p in products
            if text == (
                p["name_uz"]
                if language == "uz"
                else p["name_ru"]
            )
        ),
        None,
    )

    if not product:
        return States.CHOOSING_PRODUCT

    context.user_data["selected_product"] = product

    name = (
        product["name_uz"]
        if language == "uz"
        else product["name_ru"]
    )

    description = (
        product["description_uz"]
        if language == "uz"
        else product["description_ru"]
    )

    await update.message.reply_text(
        text=(
            f"📦 {name}\n\n"
            f"📝 {description}\n\n"
            f"🧵 Material: {product['material']}\n"
            f"💰 Price: {product['price']} UZS\n"
            f"📦 Stock: {product['stock']}"
        ),
        reply_markup=get_product_actions_keyboard(language),
    )

    return States.PRODUCT_DETAILS
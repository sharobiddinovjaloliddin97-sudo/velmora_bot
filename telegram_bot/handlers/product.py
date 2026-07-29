from telegram import Update
from telegram.ext import ContextTypes
import httpx

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

    print(product)

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

    caption = (
        f"📦 {name}\n\n"
        f"📝 {description}\n\n"
        f"🧵 Material: {product['material']}\n"
        f"💰 Price: {product['price']} UZS\n"
        f"📦 Stock: {product['stock']}"
    )

    images = product.get("images", [])

    if images:
        image_url = images[0]["image"]
        print(image_url)
        
        # Ensure we have a full URL for local testing if it's a relative path
        if not image_url.startswith("http"):
            image_url = f"http://127.0.0.1:8000{image_url}"

        try:
            # Download the image since Telegram cannot fetch from localhost
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                image_bytes = response.content

            await update.message.reply_photo(
                photo=image_bytes,
                caption=caption,
                reply_markup=get_product_actions_keyboard(language),
            )
        except Exception as e:
            print(f"Failed to load image from backend: {e}")
            await update.message.reply_text(
                text=caption,
                reply_markup=get_product_actions_keyboard(language),
            )
    else:
        await update.message.reply_text(
            text=caption,
            reply_markup=get_product_actions_keyboard(language),
        )

    return States.PRODUCT_DETAILS
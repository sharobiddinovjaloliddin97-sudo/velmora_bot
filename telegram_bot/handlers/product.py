from telegram import Update
from telegram.ext import ContextTypes

from keyboards.product_actions import get_product_actions_keyboard


async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product_name = update.message.text

    # Save the selected product
    context.user_data["selected_product"] = product_name

    await update.message.reply_text(
        text=(
            f"📦 Product: {product_name}\n\n"
            f"💰 Price: $10\n\n"
            f"Choose an action:"
        ),
        reply_markup=get_product_actions_keyboard(),
    )
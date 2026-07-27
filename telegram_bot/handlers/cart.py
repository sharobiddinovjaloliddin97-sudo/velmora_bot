from telegram import Update
from telegram.ext import ContextTypes

from keyboards.cart import get_cart_keyboard
from keyboards.main_menu import get_main_menu
from services.cart_service import CartService
from services.order_service import OrderService
from keyboards.after_add_to_cart import get_after_add_to_cart_keyboard


async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product_name = context.user_data.get("selected_product")

    if not product_name:
        await update.message.reply_text("No product selected.")
        return

    await CartService.add_product(product_name)

    await update.message.reply_text(
        text=f"✅ {product_name} added to cart.",
        reply_markup=get_after_add_to_cart_keyboard(),
    )


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cart = await CartService.get_cart()

    if not cart:
        await update.message.reply_text("🛒 Your cart is empty.")
        return

    text = "🛒 Your Cart:\n\n"

    for i, product in enumerate(cart, start=1):
        text += f"{i}. {product}\n"

    await update.message.reply_text(
        text,
        reply_markup=get_cart_keyboard(),
    )


async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await CartService.clear_cart()

    await update.message.reply_text(
        "🗑 Your cart has been cleared."
    )


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="🏠 Main Menu",
        reply_markup=get_main_menu(),
    )


async def place_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cart = await CartService.get_cart()

    if not cart:
        await update.message.reply_text(
            "🛒 Your cart is empty."
        )
        return

    order = await OrderService.create_order(cart)

    await CartService.clear_cart()

    products = "\n".join(f"• {product}" for product in order["products"])

    await update.message.reply_text(
        text=(
            f"✅ Order #{order['id']} created successfully!\n\n"
            f"📦 Products:\n"
            f"{products}\n\n"
            f"📌 Status: {order['status']}"
        )
    )
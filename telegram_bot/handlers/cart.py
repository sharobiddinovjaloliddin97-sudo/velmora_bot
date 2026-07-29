from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.texts import TEXTS
from keyboards.after_add_to_cart import get_after_add_to_cart_keyboard
from keyboards.cart import get_cart_keyboard
from keyboards.main_menu import get_main_menu
from handlers.order import place_order
from keyboards.cart_item import get_cart_inline_keyboard


from services.cart_service import CartService

from states import States


async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = context.user_data.get("selected_product")
    access_token = context.user_data.get("access")

    if not product:
        await update.message.reply_text("❌ No product selected.")
        return States.CHOOSING_PRODUCT

    print("ACCESS TOKEN:", access_token)

    await CartService.add_product(
        access_token=access_token,
        product_id=product["id"],
        quantity=1,
    )

    language = context.user_data.get("language", "uz")

    name = (
        product["name_uz"]
        if language == "uz"
        else product["name_ru"]
    )

    await update.message.reply_text(
        f"✅ {name} added to cart.",
        reply_markup=get_after_add_to_cart_keyboard(language),
    )

    return States.PRODUCT_DETAILS


async def send_cart(chat, access_token: str, language: str):
    cart = await CartService.get_cart(access_token)

    items = cart.get("items", [])

    if not items:
        messages = {
            "uz": "🛒 Savatchangiz bo'sh.",
            "ru": "🛒 Ваша корзина пуста.",
        }

        await chat.send_message(messages[language])
        return

    text = (
        "🛒 Savatcha\n\n"
        if language == "uz"
        else "🛒 Корзина\n\n"
    )

    total = 0

    for item in items:
        name = (
            item["product_name_uz"]
            if language == "uz"
            else item["product_name_ru"]
        )

        price = float(item["product_price"])
        quantity = item["quantity"]

        total += price * quantity

        text += (
            f"📦 {name}\n"
            f"💰 {price:,.0f} UZS\n"
            f"🔢 {quantity} ta\n\n"
            if language == "uz"
            else
            f"📦 {name}\n"
            f"💰 {price:,.0f} UZS\n"
            f"🔢 {quantity} шт.\n\n"
        )

    text += (
        f"━━━━━━━━━━━━━━\n"
        f"💵 Jami: {total:,.0f} UZS"
        if language == "uz"
        else
        f"━━━━━━━━━━━━━━\n"
        f"💵 Итого: {total:,.0f} UZS"
    )

    await chat.send_message(
        text=text,
        reply_markup=get_cart_inline_keyboard(
            items,
            language,
        ),
    )

    await chat.send_message(
        TEXTS[language]["choose_action"],
        reply_markup=get_cart_keyboard(language),
    )


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")

    await send_cart(
        update.effective_chat,
        access_token,
        language,
    )
    return ConversationHandler.END


async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")

    await CartService.clear_cart(access_token)

    messages = {
        "uz": "🗑 Savatcha muvaffaqiyatli tozalandi.",
        "ru": "🗑 Корзина успешно очищена.",
    }

    await update.message.reply_text(
        messages[language],
        reply_markup=get_main_menu(language),
    )

    return ConversationHandler.END


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")

    await update.message.reply_text(
        TEXTS[language]["main_menu"],
        reply_markup=get_main_menu(language),
    )

    return ConversationHandler.END




async def change_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")

    action, product_id = query.data.split(":")
    product_id = int(product_id)

    cart = await CartService.get_cart(access_token)

    item = next(
        (
            i
            for i in cart["items"]
            if i["product"] == product_id
        ),
        None,
    )

    if item is None:
        return

    quantity = item["quantity"]

    if action == "plus":
        quantity += 1

        await CartService.update_quantity(
            access_token,
            product_id,
            quantity,
        )

    else:
        quantity -= 1

        if quantity <= 0:
            await CartService.remove_product(
                access_token,
                product_id,
            )
        else:
            await CartService.update_quantity(
                access_token,
                product_id,
                quantity,
            )

    cart = await CartService.get_cart(access_token)

    items = cart.get("items", [])

    if not items:
        messages = {
            "uz": "🛒 Savatchangiz bo'sh.",
            "ru": "🛒 Ваша корзина пуста.",
        }

        await query.edit_message_text(messages[language])
        return

    text = (
        "🛒 Savatcha\n\n"
        if language == "uz"
        else "🛒 Корзина\n\n"
    )

    total = 0

    for item in items:
        name = (
            item["product_name_uz"]
            if language == "uz"
            else item["product_name_ru"]
        )

        price = float(item["product_price"])
        quantity = item["quantity"]

        total += price * quantity

        text += (
            f"📦 {name}\n"
            f"💰 {price:,.0f} UZS\n"
            f"🔢 {quantity}\n\n"
        )

    text += (
        f"━━━━━━━━━━━━━━\n"
        f"💵 {'Jami' if language == 'uz' else 'Итого'}: {total:,.0f} UZS"
    )

    await query.edit_message_text(
        text=text,
        reply_markup=get_cart_inline_keyboard(
            items,
            language,
        ),
    )
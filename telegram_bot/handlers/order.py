from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from telegram.ext import ContextTypes

from utils.texts import TEXTS
from services.order_service import OrderService
from services.cart_service import CartService
from keyboards.main_menu import get_main_menu
from keyboards.cart import get_cart_keyboard
from config import PAYMENT_PROVIDER_TOKEN, api


async def place_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data["language"]

    keyboard = [
        [
            TEXTS[language]["yes"],
            TEXTS[language]["no"],
        ]
    ]

    await update.message.reply_text(
        TEXTS[language]["confirm_order"],
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


async def confirm_order_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")

    try:
        # Create Order
        order = await OrderService.create_order(access_token)
        order_id = order.get("id")
        total_price = int(float(order.get("total_price", 0)) * 100) # Prices in Telegram are in the smallest units (tiyin for UZS)
        
        # Clear Cart
        await CartService.clear_cart(access_token)
        
        # Send Invoice if provider token exists
        if PAYMENT_PROVIDER_TOKEN:
            title = "Buyurtma to'lovi" if language == "uz" else "Оплата заказа"
            description = f"Buyurtma #{order_id} uchun to'lov" if language == "uz" else f"Оплата за заказ #{order_id}"
            
            prices = [LabeledPrice(label=title, amount=total_price)]
            
            await update.message.reply_invoice(
                title=title,
                description=description,
                payload=str(order_id),
                provider_token=PAYMENT_PROVIDER_TOKEN,
                currency="UZS",
                prices=prices,
                start_parameter="order-payment"
            )
        else:
            # Fallback if no payment token configured
            await update.message.reply_text(
                TEXTS[language]["order_success"],
                reply_markup=get_main_menu(language)
            )

    except Exception as e:
        print(f"Error creating order: {e}")
        error_msg = "Xatolik yuz berdi" if language == "uz" else "Произошла ошибка"
        await update.message.reply_text(
            error_msg,
            reply_markup=get_main_menu(language)
        )


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Something went wrong...")


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")
    access_token = context.user_data.get("access")
    
    # Update order status to paid / confirmed
    payload = update.message.successful_payment.invoice_payload
    try:
        order_id = int(payload)
        await api.patch(
            f"orders/{order_id}/",
            data={"status": "confirmed"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        msg = "✅ To'lov muvaffaqiyatli amalga oshirildi! Buyurtma tasdiqlandi." if language == 'uz' else "✅ Оплата прошла успешно! Заказ подтвержден."
        await update.message.reply_text(msg, reply_markup=get_main_menu(language))
    except Exception as e:
        print(f"Failed to update paid order {payload}: {e}")
        msg = "To'lov qabul qilindi, lekin buyurtma holatini yangilashda xatolik yuz berdi." if language == 'uz' else "Оплата принята, но произошла ошибка при обновлении статуса заказа."
        await update.message.reply_text(msg, reply_markup=get_main_menu(language))


async def confirm_order_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")
    
    await update.message.reply_text(
        TEXTS[language]["cancel"],
        reply_markup=get_cart_keyboard(language)
    )

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")

    try:
        orders = await OrderService.get_orders(access_token)
        
        if not orders:
            msg = "Sizda hozircha buyurtmalar yo'q." if language == "uz" else "У вас пока нет заказов."
            await update.message.reply_text(msg)
            return

        for order in orders:
            order_id = order.get('id', 'N/A')
            status = order.get('status', 'Pending')
            total = float(order.get('total_price', 0))
            
            text = "📦 Buyurtma / Заказ:\n\n"
            text += f"🔖 ID: #{order_id}\n"
            text += f"📊 Status: {status}\n"
            text += f"💵 Total: {total:,.0f} UZS\n"
            
            btn_text = "Batafsil" if language == "uz" else "Подробнее"
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(btn_text, callback_data=f"order_{order_id}")
            ]])
            
            await update.message.reply_text(text, reply_markup=keyboard)
    except Exception as e:
        print(f"Error fetching orders: {e}")
        error_msg = "Xatolik yuz berdi" if language == "uz" else "Произошла ошибка"
        await update.message.reply_text(error_msg)


async def order_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")
    
    order_id = int(query.data.split("_")[1])

    try:
        order = await OrderService.get_order(access_token, order_id)
        
        status = order.get('status', 'Pending')
        total = float(order.get('total_price', 0))
        items = order.get('items', [])
        
        text = f"🔖 Buyurtma / Заказ ID: #{order_id}\n"
        text += f"📊 Status: {status}\n\n"
        
        for item in items:
            name = item.get("product_name", "Mahsulot")
            qty = int(item.get("quantity", 1))
            price = float(item.get("price", 0))
            text += f"▪️ {name} x {qty} = {price * qty:,.0f} UZS\n"
            
        text += f"\n💵 Total: {total:,.0f} UZS"
        
        # We can add Cancel Order button here if status is Pending
        keyboard = []
        if status.lower() == 'pending':
            cancel_btn = "❌ Bekor qilish" if language == "uz" else "❌ Отменить"
            keyboard.append([InlineKeyboardButton(cancel_btn, callback_data=f"cancel_order_{order_id}")])
            
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Error fetching order details: {e}")
        error_msg = "Xatolik yuz berdi" if language == "uz" else "Произошла ошибка"
        await query.edit_message_text(error_msg)


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    access_token = context.user_data.get("access")
    language = context.user_data.get("language", "uz")
    
    order_id = int(query.data.split("_")[2])

    try:
        await OrderService.cancel_order(access_token, order_id)
        
        success_msg = f"✅ Buyurtma #{order_id} bekor qilindi." if language == "uz" else f"✅ Заказ #{order_id} отменен."
        await query.edit_message_text(success_msg)
    except Exception as e:
        print(f"Error canceling order: {e}")
        error_msg = "Xatolik yuz berdi" if language == "uz" else "Произошла ошибка"
        await query.edit_message_text(error_msg)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
import re

from utils.texts import TEXTS
from config import BOT_TOKEN

from states import States

from handlers.start import start
from handlers.language import choose_language
from handlers.registration import register
from handlers.catalog import catalog
from handlers.product import product
from handlers.profile import (
    profile, 
    ask_birthday, 
    save_birthday,
    ask_language,
    save_language,
    ask_phone,
    save_phone
)
from handlers.menu import main_menu
from handlers.cart import (
    add_to_cart,
    show_cart,
    clear_cart,
    back_to_main_menu,
    change_quantity,
)
from handlers.order import (
    place_order, 
    confirm_order_yes, 
    confirm_order_no, 
    my_orders, 
    order_details, 
    cancel_order,
    precheckout_callback,
    successful_payment_callback
)
from telegram.ext import PreCheckoutQueryHandler

CART_PATTERN = rf"^({re.escape(TEXTS['uz']['cart'])}|{re.escape(TEXTS['ru']['cart'])})$"

PROFILE_PATTERN = rf"^({re.escape(TEXTS['uz']['profile'])}|{re.escape(TEXTS['ru']['profile'])})$"

CATALOG_PATTERN = rf"^({re.escape(TEXTS['uz']['catalog'])}|{re.escape(TEXTS['ru']['catalog'])})$"
CATEGORIES_PATTERN = rf"^({re.escape(TEXTS['uz']['categories'])}|{re.escape(TEXTS['ru']['categories'])})$"

ADD_TO_CART_PATTERN = rf"^({re.escape(TEXTS['uz']['add_to_cart'])}|{re.escape(TEXTS['ru']['add_to_cart'])})$"

BACK_PATTERN = rf"^({re.escape(TEXTS['uz']['back'])}|{re.escape(TEXTS['ru']['back'])})$"

CLEAR_CART_PATTERN = rf"^({re.escape(TEXTS['uz']['clear_cart'])}|{re.escape(TEXTS['ru']['clear_cart'])})$"

PLACE_ORDER_PATTERN = rf"^({re.escape(TEXTS['uz']['place_order'])}|{re.escape(TEXTS['ru']['place_order'])})$"

YES_PATTERN = rf"^({re.escape(TEXTS['uz']['yes'])}|{re.escape(TEXTS['ru']['yes'])})$"
NO_PATTERN = rf"^({re.escape(TEXTS['uz']['no'])}|{re.escape(TEXTS['ru']['no'])})$"

MY_ORDERS_PATTERN = rf"^({re.escape(TEXTS['uz']['my_orders'])}|{re.escape(TEXTS['ru']['my_orders'])})$"

LANGUAGE_PATTERN = r"^(🇺🇿 O'zbek|🇷🇺 Русский)$"

MAIN_MENU_PATTERN = rf"^({re.escape(TEXTS['uz']['main_menu'])}|{re.escape(TEXTS['ru']['main_menu'])})$"

PRODUCTS_PATTERN = r"^(📦 Products)$"

app = Application.builder().token(BOT_TOKEN).build()

# ==========================
# START
# ==========================
app.add_handler(CommandHandler("start", start))

# ==========================
# REGISTRATION
# ==========================
app.add_handler(
    MessageHandler(
        filters.Regex(LANGUAGE_PATTERN),
        choose_language,
    )
)

app.add_handler(
    MessageHandler(
        filters.CONTACT,
        register,
    )
)

# ==========================
# CATALOG & CART (Conversation)
# ==========================
catalog_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.TEXT
            & (
                filters.Regex(CATALOG_PATTERN)
                | filters.Regex(CATEGORIES_PATTERN)
                | filters.Regex(r"^🔙 Kategoriyalarga qaytish$")
                | filters.Regex(r"^🔙 Назад к категориям$")
            ),
            catalog,
        ),
    ],
    states={
        States.CHOOSING_CATEGORY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                catalog,
            ),
        ],
        States.CHOOSING_PRODUCT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & ~filters.Regex(BACK_PATTERN) & ~filters.Regex(CATEGORIES_PATTERN),
                product,
            ),
            MessageHandler(
                filters.Regex(BACK_PATTERN),
                back_to_main_menu,
            ),
            MessageHandler(
                filters.Regex(CATEGORIES_PATTERN),
                catalog,
            ),
        ],
        States.PRODUCT_DETAILS: [
            MessageHandler(
                filters.Regex(ADD_TO_CART_PATTERN),
                add_to_cart,
            ),
            MessageHandler(
                filters.Regex(BACK_PATTERN),
                product,
            ),
            MessageHandler(
                filters.Regex(CATEGORIES_PATTERN) | filters.Regex(CATALOG_PATTERN),
                catalog,
            ),
        ],
    },
    fallbacks=[
        CommandHandler("start", start),
        MessageHandler(filters.Regex(MAIN_MENU_PATTERN), main_menu),
        MessageHandler(filters.Regex(CART_PATTERN), show_cart),
    ],
)
app.add_handler(catalog_conv_handler)

# ==========================
# CALLBACK QUERIES
# ==========================
app.add_handler(
    CallbackQueryHandler(
        change_quantity,
        pattern=r"^(plus|minus):",
    )
)

# ==========================
# MY ORDERS
# ==========================
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(r"^order_\d+$"),
        order_details,
    )
)
app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex(r"^cancel_order_\d+$"),
        cancel_order,
    )
)

# ==========================
# MAIN MENU
# ==========================
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(MAIN_MENU_PATTERN),
        main_menu,
    )
)

# ==========================
# CART
# ==========================
app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex(CART_PATTERN),
        show_cart,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex(CLEAR_CART_PATTERN),
        clear_cart,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex(PLACE_ORDER_PATTERN),
        place_order,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(YES_PATTERN),
        confirm_order_yes,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(NO_PATTERN),
        confirm_order_no,
    )
)

# ==========================
# PAYMENTS
# ==========================
app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

profile_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(ask_birthday, pattern=r"^set_birthday$"),
        CallbackQueryHandler(ask_language, pattern=r"^change_language$"),
        CallbackQueryHandler(ask_phone, pattern=r"^update_phone$"),
    ],
    states={
        States.WAITING_BIRTHDAY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_birthday),
        ],
        States.WAITING_LANGUAGE: [
            CallbackQueryHandler(save_language, pattern=r"^lang_(uz|ru)$"),
        ],
        States.WAITING_PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_phone),
        ],
    },
    fallbacks=[
        CommandHandler("start", start),
        MessageHandler(filters.Regex(MAIN_MENU_PATTERN), main_menu),
    ],
)
app.add_handler(profile_conversation_handler)

app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex(PROFILE_PATTERN),
        profile,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(MY_ORDERS_PATTERN),
        my_orders,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(PRODUCTS_PATTERN),
        product,
    )
)

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
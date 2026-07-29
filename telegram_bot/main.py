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
from handlers.profile import profile
from handlers.menu import main_menu
from handlers.cart import (
    add_to_cart,
    show_cart,
    clear_cart,
    back_to_main_menu,
    place_order,
    change_quantity,
)

CART_PATTERN = rf"^({re.escape(TEXTS['uz']['cart'])}|{re.escape(TEXTS['ru']['cart'])})$"

PROFILE_PATTERN = rf"^({re.escape(TEXTS['uz']['profile'])}|{re.escape(TEXTS['ru']['profile'])})$"

CATALOG_PATTERN = rf"^({re.escape(TEXTS['uz']['catalog'])}|{re.escape(TEXTS['ru']['catalog'])})$"

ADD_TO_CART_PATTERN = rf"^({re.escape(TEXTS['uz']['add_to_cart'])}|{re.escape(TEXTS['ru']['add_to_cart'])})$"

BACK_PATTERN = rf"^({re.escape(TEXTS['uz']['back'])}|{re.escape(TEXTS['ru']['back'])})$"

CLEAR_CART_PATTERN = rf"^({re.escape(TEXTS['uz']['clear_cart'])}|{re.escape(TEXTS['ru']['clear_cart'])})$"

PLACE_ORDER_PATTERN = rf"^({re.escape(TEXTS['uz']['place_order'])}|{re.escape(TEXTS['ru']['place_order'])})$"

LANGUAGE_PATTERN = r"^(🇺🇿 O'zbek|🇷🇺 Русский)$"

MAIN_MENU_PATTERN = rf"^({re.escape(TEXTS['uz']['main_menu'])}|{re.escape(TEXTS['ru']['main_menu'])})$"

PRODUCTS_PATTERN = r"^(📦 Products)$"

app = Application.builder().token(BOT_TOKEN).build()

# ==========================
# START
# ==========================
app.add_handler(
    CommandHandler(
        "start",
        start,
    )
)

# ==========================
# LANGUAGE
# ==========================
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(LANGUAGE_PATTERN),
        choose_language,
    )
)

# ==========================
# REGISTRATION
# ==========================
app.add_handler(
    MessageHandler(
        filters.CONTACT,
        register,
    )
)

# ==========================
# CONVERSATION
# ==========================
conversation_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        MessageHandler(
            filters.TEXT & filters.Regex(CATALOG_PATTERN),
            catalog,
        ),
    ],
    states={
        States.CHOOSING_CATEGORY: [
            MessageHandler(
                filters.TEXT
                & ~filters.Regex(CART_PATTERN)
                & ~filters.Regex(PROFILE_PATTERN)
                & ~filters.Regex(MAIN_MENU_PATTERN),
                catalog,
            ),
        ],

        States.CHOOSING_PRODUCT: [
            MessageHandler(
                filters.TEXT
                & ~filters.Regex(CART_PATTERN)
                & ~filters.Regex(PROFILE_PATTERN)
                & ~filters.Regex(MAIN_MENU_PATTERN),
                product,
            ),
        ],

        States.PRODUCT_DETAILS: [
            MessageHandler(
                filters.TEXT & filters.Regex(ADD_TO_CART_PATTERN),
                add_to_cart,
            ),
            MessageHandler(
                filters.TEXT & filters.Regex(BACK_PATTERN),
                product,
            ),
            MessageHandler(
                filters.TEXT & filters.Regex(CATALOG_PATTERN),
                catalog,
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            "start",
            start,
        ),
    ],
)
app.add_handler(conversation_handler)

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

# ==========================
# PROFILE
# ==========================
app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex(PROFILE_PATTERN),
        profile,
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
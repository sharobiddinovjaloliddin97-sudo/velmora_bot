from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN

from handlers.start import start
from handlers.catalog import catalog
from handlers.product import product
from handlers.profile import profile
from handlers.cart import (
    add_to_cart,
    show_cart,
    clear_cart,
    back_to_main_menu,
    place_order,
)


app = Application.builder().token(BOT_TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))

# Main Menu
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🛍 Catalog$"),
        catalog,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🛒 Cart$"),
        show_cart,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^👤 Profile$"),
        profile,
    )
)

# Catalog
app.add_handler(
    MessageHandler(
        filters.TEXT
        & filters.Regex("^(🍕 Pizza|🍔 Burger|🥤 Drinks|🔙 Categories|🔙 Back)$"),
        catalog,
    )
)

# Product
app.add_handler(
    MessageHandler(
        filters.TEXT
        & ~filters.Regex(
            "^(🛍 Catalog|🛒 Cart|👤 Profile|🛒 Add to Cart|🗑 Clear Cart|✅ Place Order|🔙 Back|🔙 Categories)$"
        ),
        product,
    )
)

# Cart
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🛒 Add to Cart$"),
        add_to_cart,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🗑 Clear Cart$"),
        clear_cart,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^✅ Place Order$"),
        place_order,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🔙 Back$"),
        back_to_main_menu,
    )
)


if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
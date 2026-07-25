from telegram import Update
from telegram.ext import ContextTypes


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        "👤 Your Profile\n\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"👤 First Name: {user.first_name}\n"
        f"👤 Last Name: {user.last_name or '-'}\n"
        f"📛 Username: @{user.username if user.username else '-'}"
    )

    await update.message.reply_text(text)
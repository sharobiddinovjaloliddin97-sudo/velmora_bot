from telegram import Update
from telegram.ext import ContextTypes

from config import api
from keyboards.main_menu import get_main_menu
from utils.texts import TEXTS

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact

    language = context.user_data.get("language", "uz")

    data = {
        "telegram_id": update.effective_user.id,
        "phone_number": contact.phone_number,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name or "",
        "language": language,
    }

    response = await api.post(
        "users/telegram-register/",
        data=data,
    )

    context.user_data["access"] = response["access"]
    context.user_data["refresh"] = response["refresh"]

    await update.message.reply_text(
        TEXTS[language]["registration_success"],
        reply_markup=get_main_menu(language),
    )
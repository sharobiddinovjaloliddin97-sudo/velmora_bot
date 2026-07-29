from telegram import Update
from telegram.ext import ContextTypes

from keyboards.registration import get_contact_keyboard
from utils.texts import TEXTS


async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🇺🇿 O'zbek":
        language = "uz"
    elif text == "🇷🇺 Русский":
        language = "ru"
    else:
        return

    # Save selected language
    context.user_data["language"] = language

    await update.message.reply_text(
        text=TEXTS[language]["share_contact"],
        reply_markup=get_contact_keyboard(),
    )
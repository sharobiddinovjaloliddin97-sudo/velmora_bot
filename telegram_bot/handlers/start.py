from telegram import Update
from telegram.ext import ContextTypes

from keyboards.language import get_language_keyboard
from utils.texts import TEXTS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Clear previous session data
    context.user_data.clear()

    await update.message.reply_text(
        text=TEXTS["uz"]["choose_language"],
        reply_markup=get_language_keyboard(),
    )
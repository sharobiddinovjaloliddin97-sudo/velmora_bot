from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards.main_menu import get_main_menu
from utils.texts import TEXTS


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")

    await update.message.reply_text(
        TEXTS[language]["main_menu"],
        reply_markup=get_main_menu(language),
    )

    return ConversationHandler.END

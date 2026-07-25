from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import get_main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Welcome to Velmora!",
        reply_markup=get_main_menu()
    )

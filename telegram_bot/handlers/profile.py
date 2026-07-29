from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
import datetime
from keyboards.profile import get_profile_keyboard
from config import api
from states import States


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    language = context.user_data.get("language", "uz")
    access_token = context.user_data.get("access")
    
    # Fetch user data from backend
    headers = {"Authorization": f"Bearer {access_token}"}
    loyalty_coins = 0
    date_of_birth = None
    try:
        backend_user = await api.get("users/me/", headers=headers)
        loyalty_coins = backend_user.get("loyalty_coins", 0)
        date_of_birth = backend_user.get("date_of_birth")
    except Exception as e:
        print(f"Failed to fetch user profile: {e}")

    text = (
        "👤 Your Profile\n\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"👤 First Name: {user.first_name}\n"
        f"👤 Last Name: {user.last_name or '-'}\n"
        f"📛 Username: @{user.username if user.username else '-'}\n\n"
        f"🎁 Loyalty Coins: {loyalty_coins} coins"
    )

    keyboard = []
    if not date_of_birth:
        if language == 'uz':
            text += "\n\n🎂 Tug'ilgan kuningizni kiriting va bizdan 50,000 UZS vaucheriga ega bo'ling!"
            btn_text = "🎂 Tug'ilgan kunni kiritish"
        else:
            text += "\n\n🎂 Введите дату рождения и получите ваучер на 50,000 UZS!"
            btn_text = "🎂 Ввести дату рождения"
            
        keyboard.append([InlineKeyboardButton(btn_text, callback_data="set_birthday")])
    else:
        if language == 'uz':
            text += f"\n🎂 Tug'ilgan kun: {date_of_birth}"
        else:
            text += f"\n🎂 Дата рождения: {date_of_birth}"

    lang_btn_text = "🌐 Tilni o'zgartirish" if language == 'uz' else "🌐 Изменить язык"
    phone_btn_text = "📱 Telefon raqamni yangilash" if language == 'uz' else "📱 Обновить номер телефона"
    
    keyboard.append([InlineKeyboardButton(lang_btn_text, callback_data="change_language")])
    keyboard.append([InlineKeyboardButton(phone_btn_text, callback_data="update_phone")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )
    # Ensure they have the profile keyboard
    await update.message.reply_text(
        "Profil sozlamalari" if language == 'uz' else "Настройки профиля",
        reply_markup=get_profile_keyboard(language)
    )


async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")]
    ]
    await query.edit_message_text(
        "Iltimos, tilni tanlang:\nПожалуйста, выберите язык:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return States.WAITING_LANGUAGE


async def save_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    new_lang = "uz" if query.data == "lang_uz" else "ru"
    context.user_data["language"] = new_lang
    
    access_token = context.user_data.get("access")
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        await api.patch("users/me/", data={"language": new_lang}, headers=headers)
    except Exception:
        pass
        
    msg = "✅ Til muvaffaqiyatli o'zgartirildi!" if new_lang == 'uz' else "✅ Язык успешно изменен!"
    await query.edit_message_text(msg)
    await query.message.reply_text("Menyu / Меню", reply_markup=get_profile_keyboard(new_lang))
    return ConversationHandler.END


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    language = context.user_data.get("language", "uz")
    
    msg = "Yangi telefon raqamingizni kiriting (Misol: +998901234567):" if language == 'uz' else "Введите ваш новый номер телефона (Пример: +998901234567):"
    await query.edit_message_text(msg)
    return States.WAITING_PHONE


async def save_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")
    access_token = context.user_data.get("access")
    new_phone = update.message.text
    
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        await api.patch("users/me/", data={"phone_number": new_phone}, headers=headers)
        msg = "✅ Telefon raqami muvaffaqiyatli yangilandi!" if language == 'uz' else "✅ Номер телефона успешно обновлен!"
    except Exception:
        msg = "❌ Xatolik yuz berdi. Balki bu raqam allaqachon banddir." if language == 'uz' else "❌ Произошла ошибка. Возможно, этот номер уже занят."
        
    await update.message.reply_text(msg, reply_markup=get_profile_keyboard(language))
    return ConversationHandler.END


async def ask_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get("language", "uz")
    if language == 'uz':
        text = "Iltimos, tug'ilgan kuningizni quyidagi formatda kiriting:\n\nYYYY-MM-DD (Misol: 2000-12-31)"
    else:
        text = "Пожалуйста, введите дату вашего рождения в формате:\n\nГГГГ-ММ-ДД (Пример: 2000-12-31)"
        
    await query.edit_message_text(text)
    return States.WAITING_BIRTHDAY


async def save_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get("language", "uz")
    access_token = context.user_data.get("access")
    text = update.message.text
    
    try:
        # Validate format
        datetime.datetime.strptime(text, "%Y-%m-%d")
        
        headers = {"Authorization": f"Bearer {access_token}"}
        await api.patch("users/me/", data={"date_of_birth": text}, headers=headers)
        
        if language == 'uz':
            msg = "✅ Tug'ilgan kuningiz muvaffaqiyatli saqlandi! Vaucher sizning tug'ilgan kuningizda avtomatik tarzda beriladi."
        else:
            msg = "✅ Дата вашего рождения успешно сохранена! Ваучер будет выдан автоматически в день вашего рождения."
            
        await update.message.reply_text(msg, reply_markup=get_profile_keyboard(language))
        return ConversationHandler.END
        
    except ValueError:
        if language == 'uz':
            msg = "❌ Noto'g'ri format. Iltimos, YYYY-MM-DD formatida kiriting (Misol: 2000-12-31):"
        else:
            msg = "❌ Неверный формат. Пожалуйста, введите в формате ГГГГ-ММ-ДД (Пример: 2000-12-31):"
            
        await update.message.reply_text(msg)
        return States.WAITING_BIRTHDAY
    except Exception as e:
        print(f"Failed to save birthday: {e}")
        if language == 'uz':
            msg = "❌ Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring."
        else:
            msg = "❌ Произошла ошибка. Пожалуйста, попробуйте еще раз."
            
        await update.message.reply_text(msg, reply_markup=get_profile_keyboard(language))
        return ConversationHandler.END
from telegram import KeyboardButton, ReplyKeyboardMarkup


def get_contact_keyboard():
    keyboard = [
        [
            KeyboardButton(
                text="📱 Share Contact",
                request_contact=True,
            )
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

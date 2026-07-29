from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.texts import TEXTS


def get_cart_inline_keyboard(items: list, language: str = "uz"):
    keyboard = []

    for item in items:
        name = (
            item["product_name_uz"]
            if language == "uz"
            else item["product_name_ru"]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"➖ {name}",
                    callback_data=f"minus:{item['product']}",
                ),
                InlineKeyboardButton(
                    f"➕ {name}",
                    callback_data=f"plus:{item['product']}",
                ),
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                TEXTS[language]["clear_cart"],
                callback_data="clear_cart",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                TEXTS[language]["place_order"],
                callback_data="place_order",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)
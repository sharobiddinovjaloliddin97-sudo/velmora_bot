"""
Conversation states for the Telegram bot.
"""

from enum import IntEnum


class States(IntEnum):
    CHOOSING_CATEGORY = 1
    CHOOSING_PRODUCT = 2
    PRODUCT_DETAILS = 3
    WAITING_BIRTHDAY = 4
    WAITING_LANGUAGE = 5
    WAITING_PHONE = 6

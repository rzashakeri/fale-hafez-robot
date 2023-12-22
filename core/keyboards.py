from telegram import ReplyKeyboardMarkup

from constants.keys import GET_OMEN

base_reply_keyboard: list = [
    [GET_OMEN],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard, resize_keyboard=True)

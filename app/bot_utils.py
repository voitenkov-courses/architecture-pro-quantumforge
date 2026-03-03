from telegram import ReplyKeyboardMarkup, KeyboardButton
from bot_config import LANGUAGES, logger

def get_main_menu_keyboard(lang: str):
    buttons = []
    buttons.extend([
        [KeyboardButton(LANGUAGES[lang]['ask_btn'])],
    ])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_cancel_keyboard(lang: str):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(LANGUAGES[lang]['cancel'])]], 
        resize_keyboard=True
    )

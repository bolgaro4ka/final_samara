from aiogram.utils.keyboard import *
from aiogram import *

def get_keyboard_mini_models():
    buttons = [

        [types.InlineKeyboardButton(text="GPT 3.5", callback_data="gpt-3.5-turbo-16k")],
        [types.InlineKeyboardButton(text="GPT 3.5 (0613)", callback_data="gpt-3.5-turbo-16k-0613")],
        [types.InlineKeyboardButton(text="GPT 4", callback_data="gpt-4-0613")],
        [types.InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

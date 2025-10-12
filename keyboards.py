from telebot import types

def general_language():
    keyboards = types.InlineKeyboardMarkup()
    btn_uz = types.InlineKeyboardButton(text="uz", callback_data="uz")
    btn_en = types.InlineKeyboardButton(text="en", callback_data="en")
    btn_ru = types.InlineKeyboardButton(text="ru", callback_data="ru")
    keyboards.row(btn_uz, btn_en, btn_ru)
    return keyboards
    
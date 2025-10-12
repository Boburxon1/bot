# from telebot import TeleBot
# from telebot import types

# token = "8390490436:AAFeWXKs29GIB50w6KA1MRzWxIYZhq0JTtE"

# bot = TeleBot(token)

# @bot.message_handler(commands="start")
# def start(message):
#     chat_id = message.chat.id
#     keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     Ozod = types.KeyboardButton(text="Salom")
#     btn_Salom = types.KeyboardButton(text="Salom")   
#     keyboards.add(btn_Salom, Ozod)
#     bot.send_message(chat_id, "Assalomu aleykum", reply_markup=keyboards) 
    
# bot.polling(none_stop=True)
    



from telebot import TeleBot
from telebot import types

token = "8390490436:AAFeWXKs29GIB50w6KA1MRzWxIYZhq0JTtE"

bot = TeleBot(token)

@bot.message_handler(commands="start")
def start(message):
    chat_id = message.chat.id
    markub = types.InlineKeyboardMarkup()
    bobur = types.InlineKeyboardButton("Bobur", url="https://t.me/itachi_bs1")
    markub.add(bobur)

    bot.send_message(chat_id, "Assalomu aleykum", reply_markup=markub)
    bot.register_next_step_handler(message, show_inline) 
    
bot.polling(none_stop=True)
def show_inline(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Bu boburni tugmasi")
    bot.polling(none_stop=True)
    
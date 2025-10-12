from telebot import TeleBot
from telebot import types
from keyboards import general_language

token = "8390490436:AAFeWXKs29GIB50w6KA1MRzWxIYZhq0JTtE"
bot = TeleBot(token)
@bot.message_handler(commands="start")
def start(message):
    chat_id = message.chat.id
    # markub = types.InlineKeyboardMarkup()
    # Bobur =  types.InlineKeyboardButton("Bobur", url ="https://t.me/ASC_MOON")
    # markub.add(Bobur)   
    bot.send_message(chat_id, "Qaysi tilda davom ettirmoqchisiz?",reply_markup=general_language()) 
    bot.send_message(chat_id, "На каком языке вы хотите продолжать?",reply_markup=general_language()) 
    bot.send_message(chat_id, "What language do you want to continue in",reply_markup=general_language()) 
    
    # bot.register_next_step_handler(call, menu_languange)

@bot.callback_query_handler(func=lambda call: True)
def menu_languange(call):
    chat_id = call.message.chat.id
    if call.data == "uz":
        bot.send_message(chat_id, "Siz o'zbek tilini tanladingiz")
    elif call.data == "ru":
        bot.send_message(chat_id, "ВЫ выбрали Руссий язык")
    elif call.data == "en":
        bot.send_message(chat_id, "You chose English")
bot.polling(none_stop=True) 



import telebot
from telebot.types import BotCommand
from keyboards import general_classes, inline_hafta_kunlari
from jadval import jadval
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN_ID")
bot = telebot.TeleBot(TOKEN)

user_data = {}

print("🤖 Bot ishga tushdi!")

def set_bot_commands():
    commands = [BotCommand("start", "Boshidan boshlash")]
    bot.set_my_commands(commands)

set_bot_commands()

@bot.message_handler(func=lambda message: True)
def testing(message):
    if message.text == '/start':
        return start(message)

    if message.text == '/admin':
        return admin(message)

# ----------------------------admin----------------------------------
@bot.message_handler(commands=['admin'])
def admin(message):
    chat_id = message.chat.id

    if chat_id == int(admin_id):
        bot.send_message(chat_id, "Admin panelga xush kelibsiz. Qaysi sinfni jadvalini o'zgartirmoqchisiz", reply_markup=general_classes())
        bot.register_next_step_handler(message, take_table)

    elif chat_id != int(admin_id):
        bot.send_message(chat_id, "Siz admin emassiz")

def take_table(message):
    chat_id = message.chat.id
    classes = [
        "5-A", "5-B", "5-D",
        "6-A", "6-B", "6-D", "6-E", "6-F",
        "7-A", "7-D", "7-E",
        "8-A", "8-B", "8-D", "8-E", "8-F",
        "9-A", "9-B", "9-D", "9-E", "9-F",
        "10-A", "10-B", "10-D", "10-G",
        "11-A", "11-D", "11-E"
    ]
    for x in classes:
        if message.text == x:
            bot.send_message(chat_id, "Yangi jadvalni kiriting: ")
            bot.register_next_step_handler(message, change_table)

def change_table(message):
    chat_id = message.chat.id
    new_table = message.text
    print(new_table)

# ----------------------------start-------------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Salom! Maktab dars jadvali botiga xush kelibsiz! 📚\n\n"
        "📌 Sinfingizni quyidagi tugmalardan tanlang:",
        reply_markup=general_classes()
    )

@bot.message_handler(func=lambda m: m.text and m.text.endswith("-sinf"))
def sinf_tanlandi(message):
    sinf = message.text[:-5]
    
    if sinf not in jadval:
        bot.send_message(message.chat.id, "❌ Kechirasiz, bu sinf uchun jadval mavjud emas.")
        return
    
    user_data[message.chat.id] = sinf
    
    # Hafta kunlari xabari
    bot.send_message(
        message.chat.id,
        f"✅ <b>{sinf}-sinf</b> muvaffaqiyatli tanlandi!\n\n"
        f"📅 Endi hafta kunini tanlang:",
        parse_mode="HTML",
        reply_markup=inline_hafta_kunlari()
    )
    remove_morkup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        ".",
        reply_markup=remove_morkup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    sinf = user_data.get(user_id)
    
    if call.data.startswith("kun_"):
        kun = call.data[4:]
        
        if not sinf:
            bot.answer_callback_query(call.id, "❗ Avval sinf tanlang!", show_alert=True)
            return
        
        darslar = jadval[sinf].get(kun, "❌ Bu kunga dars jadvali mavjud emas.")
        
        # Takroriy bosishni tekshirish
        current_text = (call.message.text or "").strip()
        new_text = (
            f"📚 <b>{sinf}-sinf</b>\n"
            f"📅 <b>{kun}</b>\n\n"
            f"{darslar}\n\n"
            f"🔄 Boshqa kunni tanlashingiz mumkin:"
        ).strip()
        
        if current_text == new_text:
            bot.answer_callback_query(call.id, f"📅 {kun} jadvali allaqachon ko‘rsatilgan ✓", show_alert=True)
            return
        
        try:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode="HTML",
                reply_markup=inline_hafta_kunlari()
            )
            bot.answer_callback_query(call.id, f"{kun} jadvali ochildi ✓")
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" in str(e):
                bot.answer_callback_query(call.id, f"📅 {kun} jadvali allaqachon ko‘rsatilgan ✓", show_alert=True)
    
    elif call.data == "back_to_classes":
        if user_id in user_data:
            del user_data[user_id]
        
        try:
            bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        except:
            pass
        
        bot.send_message(
            chat_id=user_id,
            text="🔙 Sinf tanlash menyusiga qaytdik!\n\n📌 Sinfingizni quyidagi tugmalardan tanlang:",
            reply_markup=general_classes()
        )
        bot.answer_callback_query(call.id, "Sinf tanlashga qaytdik 🔄")

@bot.message_handler(func=lambda m: m.text in ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba"])
def eski_kun(message):
    sinf = user_data.get(message.chat.id)
    if not sinf:
        bot.send_message(message.chat.id, "❗ Iltimos, avval sinf tanlang: /start")
        return
    
    kun = message.text
    darslar = jadval[sinf].get(kun, "❌ Bu kunga dars yo‘q.")
    
    bot.send_message(
        message.chat.id,
        f"📚 <b>{sinf}-sinf</b>\n📅 <b>{kun}</b>\n\n{darslar}",
        parse_mode="HTML",
        reply_markup=inline_hafta_kunlari()
    )



bot.polling(none_stop=True)
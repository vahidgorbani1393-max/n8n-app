import os
import random
import string
import telebot
from telebot import types

# توکن واقعی ربات شما
TOKEN = "9019662244:AAGuZfVgJsrqFJJZXJZ_LfTlhqoLq3wQuWc"
bot = telebot.TeleBot(TOKEN)

# دیتابیس ساده موقت برای ذخیره لایسنس‌ها
licenses = {}

def generate_license():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers1 = ''.join(random.choices(string.digits, k=4))
    numbers2 = ''.join(random.choices(string.digits, k=4))
    return f"TRD-{letters}-{numbers1}-{numbers2}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("💳 خرید اشتراک و دریافت لایسنس", callback_data="buy_sub")
    markup.add(btn_buy)
    
    bot.reply_to(
        message,
        "سلام رفیق! خوش آمدی. 🌹\nبه ربات رسمی تایید تراکنش و صدور لایسنس خوش آمدید.\nبرای خرید و دریافت کلید اختصاصی خود، روی دکمه زیر بزنید:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "buy_sub")
def callback_query(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "لطفاً مبلغ اشتراک را به کارت اعلام‌شده واریز کنید و **عکس رسید بانکی** یا کد پیگیری آن را همینجا بفرستید تا سیستم به صورت خودکار تراکنش شما را بررسی و لایسنس را صادر کند."
    )

@bot.message_handler(content_types=['photo', 'text'])
def handle_receipt(message):
    # شبیه‌سازی تایید تراکنش و صدور خودکار لایسنس
    user_id = message.from_user.id
    new_license = generate_license()
    licenses[user_id] = new_license
    
    bot.reply_to(
        message,
        f"✅ **تراکنش با موفقیت تایید شد!**\n\nبابت خرید شما متشکریم. این هم کلید لایسنس اختصاصی شما:\n`{new_license}`\n\nآن را جایی یادداشت کنید.",
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

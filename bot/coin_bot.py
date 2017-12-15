import config
import telebot
from telebot import types
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "Здравствуйте {0}. Что вы хотите? Купить или продать?".format(message.chat.first_name)
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    callback_bt1 = types.InlineKeyboardButton(text="Купить", callback_data="1")
    callback_bt2 = types.InlineKeyboardButton(text="Продать", callback_data="2")
    keyboard.add(callback_bt1, callback_bt2)
    bot.send_message(message.chat.id, welcome_msg,reply_markup=keyboard)
    


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.polling(none_stop=True)
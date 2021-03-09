from logging import exception
import telebot
from utils import CryptoConverter, APIException
from config import keys, TOKEN

TOKEN = '1667542141:AAENjvuK8bfwc76JW6VU-AxVNGxHTidoDQw'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handleStartHelp(message: telebot.types.Message):
    text = f'Welcome {message.chat.username} \nTo start working enter a command for telegramm bot in this input format: \n<Name of currency> \
<convert currency> \
<amount of currency> \nto see the list of all available currencies enter: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = f"All currencies available: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Function accept 3 parameters more was given')

        quote, base, amount = values
        total_amount = CryptoConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f"User exception \n{e}")

    except Exception as e:
        bot.reply_to(message, f"We cannot elaborete your request \n'{e} server not found' \nplease retry later")

    else:    
        text = f"Price {amount} {quote} {keys[quote]} in {base} - {total_amount[0]} {keys[base]} \ndata {total_amount[1]}"
        bot.send_message(message.chat.id, text)


bot.polling()
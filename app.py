from utils import*
from config import*
import telebot
import traceback

# Бот доступен по ссылке https://t.me/MasterCurrencyBot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = 'Приветствую вас мои повелители ☺!\nВведите команду боту в следующем формате:\n<имя валюты> ' \
           '<в какую валюту перевести> <кол-во переводимой валюты>\nНапример:\nдоллар рубль 500\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Должно быть 3 параметра, например:\nдоллар рубль 500 ')

        quote, base, amount = values

        # Если пользователь ввел буквы в разном регистре, то приравниваем в нижний
        quote = str.lower(quote)
        base = str.lower(base)

        total_base = CryptoConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        text = f'{amount} {quote} = {float(total_base) * float(amount)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
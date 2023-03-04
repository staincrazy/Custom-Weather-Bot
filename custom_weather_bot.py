from typing import Any

import telebot

from get_random_pic import get_random_picture
from open_weather_map import weather_request
from utils import getPrivateKey

bot = telebot.TeleBot(getPrivateKey('private_telegram_key.txt'))
city_info_dict = {}

__error_message = 'Something is wrong. Please, try again.'



def __reply_to(message: telebot.types.Message, img_url: str|None = None) -> None:

    # To test input in real time, please, uncomment this line of code
    # print(message.text)

    chat_id = message.chat.id

    try:
        city = message.text
        city_info_dict['city_name'] = city


        if city.lower() in ('orgrimar', 'Orgrimmar', 'orgrimmar', 'Orgri', 'Orgrimar'):
            bot.reply_to(message, 'FOR THE HORDE!!!')
            return

        bot.send_photo(chat_id, get_random_picture())

        bot.reply_to(message, get_weather(city_info_dict['city_name']))


    except Exception as e:

        bot.reply_to(message, f'Oops, this error happened - {e}. Starting over...')


@bot.message_handler(func = lambda message: True)
def welcome_message(message: Any) -> None:



    if message.text.lower() in ('/start', '/help', 'start', 'help', 'hello'):

        msg = bot.reply_to(message,
                           "Hi, i'm weather bot. To check the "
                           "weather in a desired city just type in city name. Good luck!")
        bot.register_next_step_handler(msg, process_city_step)

    elif message.text.lower() in ('/cancel', 'stop', '/stop', 'cancel', 'exit', '/exit'):

        bot.reply_to(message, "Don't stop me now....")

    else:
        __reply_to(message = message)



def process_city_step(message: Any) -> None:

    __reply_to(message)

def get_weather(city_name: str) -> str:

    weather_report = weather_request(city_name)

    if weather_report is not None:
        return weather_report

    else:

        err_msg = __error_message
        return err_msg


def runBot() -> None:
    try:
        bot.infinity_polling()
    except RuntimeError:
        print("Unhandled shut down. Experimental prototype")


# For local usage


if __name__ == '__main__':
    runBot()

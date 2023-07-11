import datetime
from typing import Any
import telebot
from random_events import get_random_picture, get_random_event, get_city_data
from open_weather_map import weather_request

from utils import getPrivateKey

bot = telebot.TeleBot(getPrivateKey('private_telegram_key.txt'))
city_info_dict = {}


def __reply_to(message: telebot.types.Message, img_url: str|None = None) -> None:

    # To test input in real time, please, uncomment this line of code
    # print(message.text)

    if img_url is None:
        img_url = get_random_picture()

    print(message.date)
    print(message.location)

    try:
        city = message.text
        city_info_dict['city_name'] = city


        if city.lower() in ('orgrimar', 'Orgrimmar', 'orgrimmar', 'Orgri', 'Orgrimar'):
            bot.reply_to(message, 'FOR THE HORDE!!!')
            return

        elif city.lower() in ('лампочка', 'lampo4ka', 'lampochka'):
            bot.reply_to(message, 'Привет, Котик! Как дела?)')
            return

        combined_reply: str = get_weather(city_info_dict['city_name']) + "\n\n" + get_city_data(city) \
                                + "\n\n" + get_random_event()

        bot.reply_to(message, combined_reply)


    except Exception as e:

        bot.reply_to(message, f'Oops, this error happened - {e}. Starting over...')


@bot.message_handler(func = lambda message: True)
def welcome_message(message: telebot.types.Message) -> None:


    if message.text.lower() in ('/start', '/help', 'start', 'help', 'hello'):

        msg = bot.reply_to(message,
                           "Hi, i'm weather bot. To check the "
                           "weather in a desired city just type in city name. Good luck!")
        bot.register_next_step_handler(msg, process_city_step)

    elif message.text.lower() in ('/cancel', 'stop', '/stop', 'cancel', 'exit', '/exit'):

        bot.reply_to(message, "Don't stop me now....")

    else:
        __reply_to(message = message)



def process_city_step(message: telebot.types.Message) -> None:

    __reply_to(message)

def get_weather(city_name: str) -> str:

    weather_report = weather_request(city_name)

    if weather_report is not None:
        return weather_report

    else:
        return  'Something is wrong. Please, try again.'


def runBot() -> None:

    try:
        bot.infinity_polling()

    except RuntimeError:

        print("Unhandled shut down. Experimental prototype")



# For local usage

if __name__ == '__main__':
    runBot()

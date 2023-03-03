from typing import Any

import telebot

from open_weather_map import weather_request
from utils import getPrivateKey

bot = telebot.TeleBot(getPrivateKey('private_telegram_key.txt'))
city_info_dict = {}

__error_message = 'Something is wrong. Please, try again.'


@bot.message_handler(func = lambda message: True)
def welcome_message(message: Any) -> None:

    # To check input in real time uncomment this line of code
    ## print(message.text)

    if message.text.lower() in ('/start', '/help', 'start', 'help', 'hello'):


        msg = bot.reply_to(message,
                           "Hi, i'm weather bot. To check the "
                           "weather in a desired city just type in city name. Good luck!")
        bot.register_next_step_handler(msg, process_city_step)

    else:
        msg = bot.reply_to(message, "To check the weather please specify city name after this message. "
                                    "What city's weather you want to know?")
        bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message: Any) -> None:

    try:
        city = message.text
        city_info_dict['city_name'] = city

        if city.lower() in ('orgrimar', 'Orgrimmar', 'orgrimmar', 'Orgri', 'Orgrimar'):
            bot.reply_to(message, 'FOR THE HORDE!!!')
            return

        bot.reply_to(message, get_weather(city_info_dict['city_name']))

    except Exception as e:

        bot.reply_to(message, f'Oops, this error happened - {e}. Starting over...')


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


if __name__ == '__main__':
    runBot()

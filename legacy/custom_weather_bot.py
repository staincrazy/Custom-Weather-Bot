import telebot

from error_logger import logEvent
from open_weather_map import weather_request
from legacy.api_utils import get_random_event, get_city_population_info, get_random_image
from private_key_utils import get_private_key


def _get_bot_inst():
    return telebot.TeleBot(get_private_key('../private_keys/private_telegram_key.txt'))


_bot = _get_bot_inst()

preserved_words = ['orgrimar', 'Orgrimmar', 'orgrimmar', 'Orgri', 'Orgrimar', 'лампочка', 'lampo4ka', 'lampochka',
                   'deepthroatovo', 'assenburg', 'assachussats', 'missititty']


def _reply_to(message: telebot.types.Message) -> None:
    print("Testing input messages: {} ".format(message.text))

    try:
        city = message.text

        if city.lower() in preserved_words:
            _bot.reply_to(message, "No longer supported, please proceed with regular city names ")
            return

        combined_reply = ("Weather section: " + "\n" + get_weather(city) +
                          "\n\n" "City population info: " + "\n" + get_city_population_info(city) +
                          "\n\n" "Random historical event section: " + "\n" + get_random_event() +
                          "\n\n" "Below we have a random image for you. Enjoy =) ")

        _bot.reply_to(message, combined_reply)
        get_random_image()
        _bot.send_photo(message.chat.id, photo=open("../img.jpg", 'rb'))

    except Exception as e:
        _bot.reply_to(message, f'Oops, nothing found ... Please, do not forget to use English characters only.')
        logEvent(e.__cause__, _reply_to, user_input=message.text)


@_bot.message_handler(func=lambda message: True)
def welcome_message(message: telebot.types.Message) -> None:
    if message.text.lower() in ('/start', '/help', 'start', 'help', 'hello'):

        msg = _bot.reply_to(message, "Hi, i'm weather bot. To check the weather in a desired city, "
                                     "just type in a city name in English. Good luck!")

        _bot.register_next_step_handler(msg, process_city_step)

    elif message.text.lower() in ('/cancel', 'stop', '/stop', 'cancel', 'exit', '/exit'):

        _bot.reply_to(message, "Don't stop me now....")

    else:
        _reply_to(message=message)


def process_city_step(message: telebot.types.Message) -> None:
    _reply_to(message)


def get_weather(city_name: str) -> str:
    weather_report = weather_request(city_name)

    return weather_report if weather_report is not None else "Something went wrong. Please, try again."


def runBot() -> None:
    try:
        _bot.infinity_polling(20)

    except RuntimeError:
        print("Unhandled shut down. Experimental prototype")


# For local testing

if __name__ == '__main__':
    runBot()

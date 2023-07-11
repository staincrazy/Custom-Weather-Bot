import requests
from get_time_zone_for_city import get_time_for_timezone
from private_key_utils import getPrivateKey

__temp = ''
__temp_feels = ''


def __celsius_to_fahrenheit(t: float | int) -> float | int:

    fahrenheit = (t * 9 / 5) + 32
    return fahrenheit

def __api_handler(url: str, city_name: str) -> str:
    my_weather_request = requests.get(url).json()

    if not my_weather_request['cod'] == '404':

        getTemp = my_weather_request['main']['temp'] - 273.15
        getTemp_feels = my_weather_request['main']['feels_like'] - 273.15

        fahrenheit_temp = str(__celsius_to_fahrenheit(getTemp))[:4]
        fahrenheit_feels_like = str(__celsius_to_fahrenheit(getTemp_feels))[:4]

        celsius_temp = str(getTemp)[:4]
        celsius_feels_like = str(getTemp_feels)[:4]

        weather_json = my_weather_request['weather']
        weather_main = weather_json[0]['main']

        weather_description_json = my_weather_request['weather']
        weather_description = weather_description_json[0]['description']

        return f'At {get_time_for_timezone(city_name)} in {city_name} current temperature is ' \
               f'{celsius_temp} Celsius / {fahrenheit_temp} Fahrenheit ' \
               f'(feels like {celsius_feels_like} C / {fahrenheit_feels_like} F). ' \
               f' The weather is ' \
               f'{weather_main} ({weather_description})'

    elif my_weather_request['cod'] == '404':
        return "City not found. Please, try again."


def weather_request(city_name: str) -> str|None:

    my_key = getPrivateKey('private_owm_key.txt')

    url = f"https://api.openweathermap.org/data/2.5/weather?appid={my_key}&q={city_name}"

    try:
        return __api_handler(url, city_name)

    except TypeError:
        return None




###====================TEST CODE HERE======================###
def code_test():
    print('Paste here function you need to test')
    print(weather_request('Manchester'))


if __name__ == '__main__':
    code_test()
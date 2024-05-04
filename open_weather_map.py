import requests
from get_time_zone_for_city import get_time_for_timezone
from private_key_utils import get_private_key

_t = ''
_t_feels_like = ''


def _celsius_to_fahrenheit_converter(t: float | int) -> float | int:
    return (t * 9 / 5) + 32


def _api_handler(url: str | None = None, city_name: str | None = None) -> str:
    if None in (url, city_name) or not all(isinstance(i, str) for i in [url, city_name]):
        raise TypeError("City Name and URL should be provided as string")

    my_weather_request = requests.get(url).json()

    if my_weather_request['cod'] == 400:
        return "City not found. Please, try again."

    temp = my_weather_request['main']['temp']
    temp_feels_like = my_weather_request['main']['feels_like']

    get_temp = temp - 273.15
    get_temp_feels = temp_feels_like - 273.15

    fahrenheit_temp = str(_celsius_to_fahrenheit_converter(get_temp))[:4]
    fahrenheit_feels_like = str(_celsius_to_fahrenheit_converter(get_temp_feels))[:4]

    celsius_temp = str(get_temp)[:4]
    celsius_feels_like = str(get_temp_feels)[:4]

    weather_json = my_weather_request['weather']
    weather_main = weather_json[0]['main']
    weather_description = weather_json[0]['description']

    return f'At {get_time_for_timezone(city_name)} in {city_name} current temperature is ' \
           f'{celsius_temp} Celsius / {fahrenheit_temp} Fahrenheit ' \
           f'(feels like {celsius_feels_like} C / {fahrenheit_feels_like} F). ' \
           f' The weather is ' \
           f'{weather_main} ({weather_description})'


def weather_request(city_name: str) -> str:
    my_key = get_private_key('private_owm_key.txt')
    url = f"https://api.openweathermap.org/data/2.5/weather?appid={my_key}&q={city_name}"
    return _api_handler(url, city_name)


if __name__ == '__main__':
    def code_test():
        ### 'Paste here function you need to test' ###
        print(weather_request("Минск"))


    code_test()

from datetime import datetime
import requests

from utils import getPrivateKey

__temp = ''
__temp_feels = ''


def celsius_to_fahrenheit(t):
    fahrenheit = (t * 9 / 5) + 32
    return fahrenheit


def weather_request(city_name, degree):
    my_key = getPrivateKey('private_owm_key.txt')
    url = f"https://api.openweathermap.org/data/2.5/weather?appid={my_key}&q={city_name}"

    try:
        return api_handler(url, city_name, degree)
    except TypeError:
        return None


def api_handler(url, city_name, degree):
    response = requests.get(url)
    my_weather_request = response.json()

    if not my_weather_request['cod'] == '404':

        getTemp = my_weather_request['main']['temp'] - 273.15
        getTemp_feels = my_weather_request['main']['feels_like'] - 273.15

        if degree.lower() == 'fahrenheit':

            temp = str(celsius_to_fahrenheit(getTemp))[:4]
            temp_feels = str(celsius_to_fahrenheit(getTemp_feels))[:4]

        elif degree.lower() == 'celsius':

            temp = str(getTemp)[:4]
            temp_feels = str(getTemp_feels)[:4]

        else:
            raise TypeError('Please, provide correct degree')

        weather_json = my_weather_request['weather']
        weather_main = weather_json[0]['main']
        weather_description_json = my_weather_request['weather']
        weather_description = weather_description_json[0]['description']

        return f'For time: {datetime.now().strftime("%H:%m")} in {city_name} current temperature is ' \
               f'{temp} {degree.capitalize()} (feels like {temp_feels}), the weather is ' \
               f'{weather_main} ({weather_description})'

    elif my_weather_request['cod'] == '404':
        return "City not found. Please, try again."


# Here you can test OWM endpoint directly
if __name__ == '__main__':
    pass

import random
import shutil

import requests
from private_key_utils import get_private_key

private_key = get_private_key('private_api_ninjas_key.txt')
_url_cities = "https://api.api-ninjas.com/v1/city?name={}"
_url_years = "https://api.api-ninjas.com/v1/historicalevents?year={}"
_url_rand_image = "https://api.api-ninjas.com/v1/randomimage"  # ?category=nature"


def get_city_lng(city_name: str) -> int | None:
    try:
        return requests.get(_url_cities.format(city_name), headers={'X-Api-Key': private_key}).json()[0]['longitude']
    except Exception as e:
        print(f"Log error {e}")
        return None


def get_city_lat(city_name: str) -> int | None:
    try:
        return requests.get(_url_cities.format(city_name), headers={'X-Api-Key': private_key}).json()[0]['latitude']
    except Exception as e:
        print(f"Log error {e}")
        return None


def get_city_population_info(city_name: str | None = None) -> str:
    if city_name is None and not isinstance(city_name, str):
        raise TypeError("City Name should be provided as string")

    try:
        response = requests.get(_url_cities.format(city_name), headers={'X-Api-Key': private_key})
    except Exception as e:
        return f"Something is wrong. Please refer to the error {e}"

    city_name = response.json()[0]['name']
    country_name = response.json()[0]['country']
    population = response.json()[0]['population']

    return f'Just in case you forgot: {city_name} is the city of {country_name} ' \
           f'with the population of {population} ppl'


def get_random_event(year: int | None = None) -> str:
    if year is None:
        year = random.randint(-351, 2023)

    try:
        e = requests.get(_url_years.format(year), headers={'X-Api-Key': private_key}).json()[0]['event']
        return f'Did you know that in year: {year} - {e}'
    except Exception as e:
        print(f"Check the error {e}")
        return "Nothing to show this time"


def get_random_image():
    response = requests.get(_url_rand_image, headers={'X-Api-Key': private_key, 'Accept': 'image/jpg'})

    if response.status_code == 200:
        with open('img.jpg', 'wb') as out_file:
            out_file.write(response.content)


if __name__ == '__main__':
    print(get_random_image())

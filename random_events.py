import random

import requests

from utils import getPrivateKey

private_key = getPrivateKey('private_api_ninjas_key.txt')

def get_city_data(city_name: str|None = None) -> str:

    if city_name is not None:

        response = requests.get("https://api.api-ninjas.com/v1/city?name={}".format(city_name),
                            headers={'X-Api-Key': private_key})

        city_name = response.json()[0]['name']
        country_name = response.json()[0]['country']
        population = response.json()[0]['population']

        return  f'Just in case you forgot: {city_name} is the city of {country_name} ' \
                f'with the population of {population} ppl'


def get_random_picture():

    img_url = "https://random.imagecdn.app/500/150"
    return img_url


def get_random_event(year: int|None = None) -> str:

    if year is None:
        year = random.randint(-351,2023)

    event: str|None = None

    response = requests.get(f"https://api.api-ninjas.com/v1/historicalevents?year={year}",
                            headers={'X-Api-Key': private_key})

    if len(response.json())>0:
        event = response.json()[0]['event']


    if event is None:
            return 'No fun facts this time...'

    return f'Did you know that in {year} - {event}'


## This line of code can be used for requests testing

if __name__ == '__main__':
    print(get_city_data("Minsk"))

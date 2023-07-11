import random
import requests
from private_key_utils import getPrivateKey

private_key = getPrivateKey('private_api_ninjas_key.txt')

def get_city_lng(city_name: str) -> int|None:

    try:
        return requests.get("https://api.api-ninjas.com/v1/city?name={}".format(city_name),
                                headers={'X-Api-Key': private_key}).json()[0]['longitude']

    except:
        return None

def get_city_lat(city_name: str) -> int|None:

    try:
        return requests.get("https://api.api-ninjas.com/v1/city?name={}".format(city_name),
                            headers={'X-Api-Key': private_key}).json()[0]['latitude']

    except:
        return None

def get_city_population_info(city_name: str|None = None) -> str:

    city_name = str(city_name)

    if city_name is not None:

        response = requests.get("https://api.api-ninjas.com/v1/city?name={}".format(city_name),
                            headers={'X-Api-Key': private_key})

        try:

            city_name = response.json()[0]['name']
            country_name = response.json()[0]['country']
            population = response.json()[0]['population']

            return  f'Just in case you forgot: {city_name} is the city of {country_name} ' \
                    f'with the population of {population} ppl'
        except:

            return f'No information was found for this city - "{city_name}" =/'



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


###====================TEST CODE HERE======================###
def code_test():
    print('Paste here function you want to test')
    print(get_city_population_info('Tbilisi'))


if __name__ == '__main__':
    code_test()
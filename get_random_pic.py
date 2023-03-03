import random
from typing import Any
import shutil


import requests

from utils import getPrivateKey



private_key = getPrivateKey('private_api_ninjas_key.txt')
url = "https://picsum.photos/600"

def __get_city_pic_url(city_name: str|None = None) -> None:

    if city_name is not None:

        response = requests.get("https://api.api-ninjas.com/v1/randomimage?category=City",
                            headers={'X-Api-Key': private_key, 'Accept': 'image/jpg'})


        with open('img.png', 'wb') as out_file:

            shutil.copyfileobj(response.raw, out_file)

            out_file.close()





def get_random_picture():

    img_url = "https://random.imagecdn.app/500/150"

    return img_url








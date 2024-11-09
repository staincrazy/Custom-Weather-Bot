from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from legacy.api_utils import get_city_lng, get_city_lat
from datetime import datetime


def _get_timezone(city_name: str) -> str | None:
    tz = TimezoneFinder()
    lng = get_city_lng(city_name)
    lat = get_city_lat(city_name)

    return tz.timezone_at(lng=lng, lat=lat) if None not in (lat, lng) else None


def get_time_for_timezone(city_name: str) -> str | None:
    zone = _get_timezone(city_name)

    return datetime.now(tz=ZoneInfo(zone)).strftime("%H-%M") if zone is not None \
        else datetime.now().strftime("%H-%M")


###====================TEST CODE HERE======================###
def code_test():
    print('Paste here function you want to test')
    print(get_time_for_timezone('Jooisoas'))
    print(get_time_for_timezone('London'))


if __name__ == '__main__':
    code_test()

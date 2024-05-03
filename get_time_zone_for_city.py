from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from api_utils import get_city_lng, get_city_lat
from datetime import datetime


def _get_timezone(city_name: str) -> str|None:
    tz = TimezoneFinder()

    try:
        lng = get_city_lng(city_name)
    except:
        lng = None

    try:
        lat = get_city_lat(city_name)
    except:
        lat = None

    if None not in (lat, lng):
        return tz.timezone_at(lng=lng, lat=lat)

    else:
        return None


def __get_current_server_time() -> datetime | str:
    return datetime.now().strftime("%H-%M")

def get_time_for_timezone(city_name: str) -> str | None:
    zone = _get_timezone(city_name)

    if zone is not None:
        return datetime.now(tz=ZoneInfo(zone)).strftime("%H-%M")

    return __get_current_server_time()


###====================TEST CODE HERE======================###
def code_test():
    print('Paste here function you want to test')
    print(get_time_for_timezone('Jooisoas'))
    print(get_time_for_timezone('London'))


if __name__ == '__main__':
    code_test()

import pytz
import requests
import json
import time
from datetime import datetime, timedelta, timezone

POSITION_API = 'http://api.open-notify.org/iss-now.json'
SUNSET_SUNRISE_API = 'https://api.sunrise-sunset.org/json'

SS_API_TIME_PARSE_STRING = '%Y-%m-%dT%H:%M:%S'


def get_position():
    response = requests.get(POSITION_API)
    if response.status_code != 200:
        print(f'Received status code {response.status_code} from Position API')
        return None, None, None
    else:
        data = response.json()
        return data['timestamp'], data['iss_position']['latitude'], data['iss_position']['longitude']


def get_sunrise_sunset(latitude, longitude):
    response = requests.get(SUNSET_SUNRISE_API + f'?lat={latitude}&lng={longitude}&date=today&formatted=0')
    if response.status_code != 200:
        print(f'Received status code {response.status_code} from Sunset Sunrise API')
        return None, None, None
    else:
        data = response.json()['results']
        sunrise = data['sunrise'][:-6] # strip timezone
        sunset = data['sunset'][:-6]
        return sunrise, sunset


def print_stuff(sunrise, sunset, timestamp):
    sunrise_date = datetime.strptime(sunrise, SS_API_TIME_PARSE_STRING).replace(tzinfo=timezone.utc)
    sunset_date = datetime.strptime(sunset, SS_API_TIME_PARSE_STRING).replace(tzinfo=timezone.utc)
    current_date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)

    sunrise_minus_two_h = sunrise_date - timedelta(hours=2)
    sunrise_minus_one_h = sunrise_date - timedelta(hours=1)
    sunset_plus_one_h = sunset_date + timedelta(hours=1)
    sunset_plus_two_h = sunset_date + timedelta(hours=2)

    if sunrise_date <= current_date <= sunset_date:
        print(f'[{current_date}] The ISS IS on the illuminated side of the earth')
    else:
        print(f'[{current_date}] The ISS IS NOT on the illuminated side of the earth')

    if sunrise_minus_two_h <= current_date <= sunrise_minus_one_h or \
            sunset_plus_one_h <= current_date <= sunset_plus_two_h:
        print(f'[{current_date}] Ideal conditions for observation')


def main():
    while True:
        timestamp, lat, lng = get_position()
        if timestamp is None:
            time.sleep(2)
            continue
        sunrise, sunset = get_sunrise_sunset(lat, lng)
        if sunrise is None:
            time.sleep(2)
            continue
        print_stuff(sunrise, sunset, timestamp)
        time.sleep(5)


if __name__ == '__main__':
    main()

import requests
import json
import time
from datetime import datetime

POSITION_API = 'http://api.open-notify.org/iss-now.json'
SUNSET_SUNRISE_API = 'https://api.sunrise-sunset.org/json'

SS_API_TIME_PARSE_STRING = '%Y-%m-%d %I:%M:%S %p'

ONE_HOUR = 3600
TWO_HOURS = 7200


def get_position():
    response = requests.get(POSITION_API)
    if response.status_code != 200:
        print(f'Received status code {response.status_code} from Position API')
        return None, None, None
    else:
        data = response.json()
        return data['timestamp'], data['iss_position']['latitude'], data['iss_position']['longitude']


def get_sunrise_sunset(latitude, longitude):
    response = requests.get(SUNSET_SUNRISE_API + f'?lat={latitude}&lng={longitude}&date=today')
    if response.status_code != 200:
        print(f'Received status code {response.status_code} from Sunset Sunrise API')
        return None, None, None
    else:
        data = response.json()['results']
        sunrise = data['sunrise']
        sunset = data['sunset']
        day_length = data['day_length']
        return sunrise, sunset, day_length


def print_stuff(sunrise, sunset, timestamp):
    sunrise = '1970-1-1 ' + sunrise
    sunset = '1970-1-1 ' + sunset
    sunrise_timestamp = time.mktime(datetime.strptime(sunrise, SS_API_TIME_PARSE_STRING).timetuple())
    sunset_timestamp = time.mktime(datetime.strptime(sunset, SS_API_TIME_PARSE_STRING).timetuple())
    today_timestamp = time.mktime(datetime.date(datetime.now()).timetuple())
    sunrise_timestamp = today_timestamp + sunrise_timestamp
    sunset_timestamp = today_timestamp + sunset_timestamp

    if sunrise_timestamp <= timestamp <= sunset_timestamp:
        print('The ISS IS on the illuminated side of the earth')
    else:
        print('The ISS IS NOT on the illuminated side of the earth')

    if sunrise_timestamp - TWO_HOURS <= timestamp <= sunrise_timestamp - ONE_HOUR or \
            sunset_timestamp + ONE_HOUR <= timestamp <= sunset_timestamp + TWO_HOURS:
        print('Ideal conditions for earth observation')


def main():
    while True:
        timestamp, lat, lng = get_position()
        if timestamp is None:
            time.sleep(2)
            continue
        sunrise, sunset, day_length = get_sunrise_sunset(lat, lng)
        if sunrise is None:
            time.sleep(2)
            continue
        print_stuff(sunrise, sunset, timestamp)
        time.sleep(5)


if __name__ == '__main__':
    main()

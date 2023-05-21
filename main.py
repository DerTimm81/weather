from wl_connection import WeatherLink
from pprint import pprint
import configparser

config = configparser.ConfigParser()

# Fill out the 'config_sample.ini' with meaningful content and remove the '_sample'-phrase in the filename, so you get your own 'config.ini'
# From this point on, you will see your own stuff.
config.read('config.ini')

API_KEY = config['API']['ApiKey']
API_SECRET = config['API']['ApiSecret']


# Create a WeatherLink object using API keys
wl = WeatherLink(API_KEY, API_SECRET)

stations = wl.stations().json()
station_id = stations['stations'][0]['station_id']

current_data = wl.current(station_id).json()


inside_temp = current_data['sensors'][0]['data'][0]['temp_in']
inside_temp_celsius = (inside_temp - 32) * 5/9
print('Inside Temperature is at: ' + str(inside_temp_celsius) + ' °C')

outside_temp = current_data['sensors'][1]['data'][0]['temp']
outside_temp_celsius = (outside_temp - 32) * 5/9
print('Outside Temperature is at: ' + str(outside_temp_celsius) + ' °C')
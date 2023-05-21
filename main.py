from wl_connection import WeatherLink
from pprint import pprint
import configparser

import logging
import time

import weatherlink_live_local as wlll

logging.basicConfig(level=logging.ERROR)

config = configparser.ConfigParser()

# Fill out the 'config_sample.ini' with meaningful content and remove the '_sample'-phrase in the filename, so you get your own 'config.ini'
# From this point on, you will see your own stuff.
config.read('config.ini')

API_KEY = config['API']['ApiKey']
API_SECRET = config['API']['ApiSecret']

if config['API']['ConnectToWeatherLinkServer'] == "True":

    print("Trying to connect to your WeatherLink account (via Internet) ...")

    # Create a WeatherLink object using API keys
    wl = WeatherLink(API_KEY, API_SECRET)

    stations = wl.stations().json()
    station_id = stations['stations'][0]['station_id']

    current_data = wl.current(station_id).json()


    inside_temp = current_data['sensors'][0]['data'][0]['temp_in']
    inside_temp_celsius = (inside_temp - 32) * 5/9
    print(f"Inside Temperature is at: {inside_temp_celsius:.2f} °C")

    outside_temp = current_data['sensors'][1]['data'][0]['temp']
    outside_temp_celsius = (outside_temp - 32) * 5/9
    print(f"Outside Temperature is at: {outside_temp_celsius:.2f} °C")

if config['API']['ConnectToLocalWeatherLink'] == "True":
    print("Trying to connect to WeatherLink in your network (just using local wifi)...")

    devices = wlll.discover()
    # print(devices)

    # select first device, get IP address
    ip_first_device = devices[0].ip_addresses[0]

    # specify units
    wlll.set_units(
        temperature=wlll.units.TemperatureUnit.CELSIUS,
        pressure=wlll.units.PressureUnit.HECTOPASCAL,
        rain=wlll.units.RainUnit.MILLIMETER,
        wind_speed=wlll.units.WindSpeedUnit.METER_PER_SECOND,
    )

    conditions = wlll.get_conditions(ip_first_device)
    print(f"Inside temperature:  {conditions.inside.temp:.2f} °C")
    print(f"Outside temperature: {conditions.integrated_sensor_suites[0].temp:.2f} °C")

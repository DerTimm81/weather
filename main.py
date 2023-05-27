from WeatherLink_Server.wl_remote_connect import WeatherLink_Server 
import weatherlink_live_local as WeatherLink_Local

from pprint import pprint
import configparser

import logging
import time



# we will avoid using "print"-statements but instead work with the logging-functionality of Python
# setting the below to "logging.INFO" will bring up all details.
# if you want to go for production, please change for "logging.ERROR"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

1
config = configparser.ConfigParser()

# Fill out the 'config_sample.ini' with meaningful content 
# and remove the '_sample'-phrase in the filename, so you get your own 'config.ini'
# From this point on, you will see your own stuff.
config.read('config.ini')

# reading the API key and secret from the configuration file
API_KEY = config['API']['ApiKey']
API_SECRET = config['API']['ApiSecret']

# trying to access the WeatherLink Live Server to retrieve the weather data from your weather station
if config['API']['ConnectToWeatherLinkServer'] == "True":

    logger.info(f"Trying to connect to your WeatherLink account (via Internet) ...")

    # Create a WeatherLink object using API keys
    wl = WeatherLink_Server(API_KEY, API_SECRET)

    # getting the list of stations associated in account
    # taking the first station (will work for most configs) and get it's ID as its needed below
    stations = wl.stations().json()
    station_id = stations['stations'][0]['station_id']

    # getting current weather data
    current_data = wl.current(station_id).json()

    # getting the inside temperature and converting it to Celsius
    inside_temp = current_data['sensors'][0]['data'][0]['temp_in']
    inside_temp_celsius = (inside_temp - 32) * 5/9
    logger.info(f"Inside Temperature is at: {inside_temp_celsius:.2f} °C")

    # getting the outside temperature and converting it to Celsius
    outside_temp = current_data['sensors'][1]['data'][0]['temp']
    outside_temp_celsius = (outside_temp - 32) * 5/9
    logger.info(f"Outside Temperature is at: {outside_temp_celsius:.2f} °C")

# trying to connect to local weather station via local network
if config['API']['ConnectToLocalWeatherLink'] == "True":
    
    logger.info(f"Trying to connect to WeatherLink in your network (just using local wifi)...")

    # We are using a library, which you should install via pip
    # for for 'pip install weatherlink_live_local", and you can use it right away
    devices = WeatherLink_Local.discover()

    # select first device, get IP address
    ip_first_device = devices[0].ip_addresses[0]

    # set some European units
    WeatherLink_Local.set_units(
        temperature=WeatherLink_Local.units.TemperatureUnit.CELSIUS,
        pressure=WeatherLink_Local.units.PressureUnit.HECTOPASCAL,
        rain=WeatherLink_Local.units.RainUnit.MILLIMETER,
        wind_speed=WeatherLink_Local.units.WindSpeedUnit.METER_PER_SECOND,
    )

    # get current weather conditions
    conditions = WeatherLink_Local.get_conditions(ip_first_device)

    logger.info(f"Inside temperature:  {conditions.inside.temp:.2f} °C")
    logger.info(f"Outside temperature: {conditions.integrated_sensor_suites[0].temp:.2f} °C")

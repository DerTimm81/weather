########################################################################################################################
# 
########################################################################################################################

import time
import hmac
import hashlib
import requests
import collections


class WeatherLink_Server:

    API_URL_V2 = 'https://api.weatherlink.com/v2/'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret.encode('utf-8')
        self.timestamp = int(time.time())

    def signature(self, params={}):
        self.timestamp = int(time.time())

        params['api-key'] = self.api_key
        params['t'] = self.timestamp

        params = collections.OrderedDict(sorted(params.items()))

        payload = ''
        for key in params:
            payload = payload + key + str(params[key])

        return hmac.new(self.api_secret, payload.encode('utf-8'), hashlib.sha256).hexdigest()

    def stations(self, station_ids=[]):
        stations_str = ','.join(station_ids)
        query_params = {
            'api-key': self.api_key,
            'api-signature': self.signature({'station-ids': stations_str} if station_ids else {}),
            't': str(self.timestamp)
        }
        return requests.get(self.API_URL_V2 + 'stations/' + stations_str, params=query_params)

    def current(self, station_id):
        query_params = {
            'api-key': self.api_key,
            'api-signature': self.signature({'station-id': station_id}),
            't': str(self.timestamp)
        }
        return requests.get(self.API_URL_V2 + 'current/' + str(station_id), params=query_params)
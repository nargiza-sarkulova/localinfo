# -*- coding: utf-8 -*-
from django.conf import settings

from clients.base import BaseClient


class OpenWeatherAPIClient(BaseClient):
    """
    OpenWeatherMap API client
    @see: https://openweathermap.org/current
    """

    def __init__(self):
        self.base_url = ('http://api.openweathermap.org/data/2.5/weather?'
                         'lat={lat}&lon={lon}&APPID={api_key}')

    def get_weather_info(self, latitude, longitude):
        url = self.base_url.format(lat=latitude, lon=longitude,
                                   api_key=settings.OPEN_WEATHER_API_KEY)
        info = self._make_request(url)
        if info:
            return {
                'description': info.get('weather')[0].get('description').capitalize(),
                'temperature': info.get('main', {}).get('temp'),
                'pressure': info.get('main', {}).get('pressure'),
                'humidity': info.get('main', {}).get('humidity'),
                'wind_speed': info.get('wind', {}).get('speed')
            }
        return None

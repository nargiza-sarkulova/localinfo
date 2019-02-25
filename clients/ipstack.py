# -*- coding: utf-8 -*-
from django.conf import settings

from clients.base import BaseClient


class IPstackAPIClient(BaseClient):
    """
    IPstack API client
    @see: https://ipstack.com/documentation
    """

    def __init__(self):
        self.base_url = 'http://api.ipstack.com/{ip_number}?access_key={api_key}'

    def get_ip_info(self, ip_number):
        url = self.base_url.format(ip_number=ip_number, api_key=settings.IPSTACK_API_KEY)
        info = self._make_request(url)
        if info:
            return {
                'number': info.get('ip'),
                'country_name': info.get('country_name'),
                'country_code': info.get('country_code'),
                'country_flag': info.get('location', {}).get('country_flag'),
                'region_name': info.get('region_name'),
                'city': info.get('city'),
                'latitude': info.get('latitude'),
                'longitude': info.get('longitude')
            }
        return None

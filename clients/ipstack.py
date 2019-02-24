# -*- coding: utf-8 -*-
import json
import logging
import requests

from django.conf import settings


logger = logging.getLogger(__name__)


class BaseClient:
    def _make_request(self, url):
        logger.debug("Sending request to '%s'...", url)
        response = requests.get(url)

        if response.status_code != 200:
            logger.error("Error retrieving data from API: status_code(%d)", response.status_code)
            logger.debug(response.text)
            return None
        return response.json()


class IPstackAPIClient(BaseClient):
    """
    IPstack API client
    @see: https://ipstack.com/documentation
    """

    def __init__(self):
        self.base_url = 'http://api.ipstack.com/{ip_number}?access_key={access_key}'

    def get_ip_info(self, ip_number):
        url = self.base_url.format(ip_number=ip_number, access_key=settings.IPSTACK_ACCESS_KEY)
        info = self._make_request(url)
        if info:
            return {
                'number': info.get('ip'),
                'country_name': info.get('country_name'),
                'country_flag': info.get('location', {}).get('country_flag'),
                'region_name': info.get('region_name'),
                'city': info.get('city'),
                'latitude': info.get('latitude'),
                'longitude': info.get('longitude')
            }
        return None

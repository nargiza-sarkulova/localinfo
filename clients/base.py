# -*- coding: utf-8 -*-
import logging
import requests


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

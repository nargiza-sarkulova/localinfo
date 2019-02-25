# -*- coding: utf-8 -*-
from django.conf import settings

from clients.base import BaseClient


PAGE_SIZE = 5


class NewsAPIClient(BaseClient):
    """
    News API client
    @see: https://newsapi.org/docs/endpoints/top-headlines
    """

    def __init__(self):
        self.base_url = ('https://newsapi.org/v2/top-headlines?apiKey={api_key}&'
                         'country={country_code}&pageSize={page_size}')

    def get_news(self, country_code):
        url = self.base_url.format(country_code=country_code, api_key=settings.NEWS_API_KEY,
                                   page_size=PAGE_SIZE)
        info = self._make_request(url)
        if info:
            return info['articles']
        return None

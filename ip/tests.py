# -*- coding: utf-8 -*-
from decimal import Decimal
from mock import patch
from django_redis import get_redis_connection

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ip.models import IP
from clients.ipstack import IPstackAPIClient
from clients.news import NewsAPIClient
from clients.open_weather import OpenWeatherAPIClient


class IPTest(TestCase):
    def test_ip_uniqueness(self):
        """
        Test IP number is unique accross table
        """
        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'country_code': 'ca',
            'region_name': 'Ontario',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip1 = IP(**data)
        ip1.save()

        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'country_code': 'ca',
            'region_name': 'Ontario',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip2 = IP(**data)
        self.assertRaises(IntegrityError, ip2.save)


def _mock_ip_info(self, ip_number):
    data = {'174.114.57.161': {'number': '174.114.57.161',
                               'country_name': 'Canada',
                               'country_code': 'ca',
                               'region_name': 'Ontario',
                               'city': 'Ottawa',
                               'latitude': '67.4289',
                               'longitude': '-82.6844'},
            '174.114.57.162': {'number': '174.114.57.162',
                               'country_name': 'Canada',
                               'country_code': 'ca',
                               'region_name': 'Ontario',
                               'latitude': '60.7543',
                               'longitude': '-90.6844'},
            '174.114.57.163': {'number': '174.114.57.162',
                               'country_name': 'Canada',
                               'country_code': 'ca',
                               'region_name': 'Ontario',
                               'latitude': 'XXXX33',
                               'longitude': '-90.6844'}}
    return data.get(ip_number)


def _mock_weather_info(self, latitude, longitude):
    return {
        'description': 'Light shower snow',
        'temperature': 274.78,
        'pressure': 985,
        'humidity': 86,
        'wind_speed': 9.3
    }

def _mock_news(self, country_code):
    return [{'source': {'id': '',
                        'name': "Castanet.net"},
             'author': '',
             'title': "Cases of measles rising - BC News - Castanet.net",
             'description': "UPDATE: 5:20 p.m. Two new cases of measles were reported.",
             'url': "https://www.castanet.net/edition/news-story-250012-3-.htm",
             'urlToImage': "https://www.castanet.net/content/2019/2/screen_shot_2019-02-24_at_1.48.44_pm_p3371823.jpg",
             'publishedAt': "2019-02-25T01:22:00Z",
             'content': "BC UPDATE: 5:20 p.m. Two new cases … [+21551 chars]"},
            {'source': {'id': '',
                        'name': "Raptorshq.com"},
             'author': "Jacob M. Mack",
             'title': "Listless Raptors falter in 113-98 loss to Orlando - RaptorsHQ",
             'description': "A punchless bench unit and 3:30 start seemed the main culprits as the Raptors lost the Magic at home",
             'url': "https://www.raptorshq.com/2019/2/24/18238927/toronto-raptors-orlando-magic-final-score-recap",
             'urlToImage': "https://cdn.vox-cdn.com/thumbor/2o5U3d2-dMfbRvF__TRJKbfs0M0=/0x0:2456x1286/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/14470764/usa_today_12229165.jpg",
             'publishedAt': "2019-02-24T23:34:37Z",
             'content': "A Sunday afternoon game … [+5777 chars]"}]


@patch.object(IPstackAPIClient, 'get_ip_info', _mock_ip_info)
@patch.object(OpenWeatherAPIClient, 'get_weather_info', _mock_weather_info)
@patch.object(NewsAPIClient, 'get_news', _mock_news)
class IpAPITest(APITestCase):

    def tearDown(self, *args, **kwargs):
        super(IpAPITest, self).tearDown(*args, **kwargs)
        get_redis_connection('default').flushall()

    def test_create_ip(self):
        """
        Create new IP
        """
        url = reverse('ip-list')
        data = {'number': '174.114.57.161'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IP.objects.count(), 1)
        self.assertEqual(IP.objects.get().number, '174.114.57.161')
        self.assertEqual(IP.objects.get().country_name, 'Canada')
        self.assertEqual(IP.objects.get().country_code, 'ca')
        self.assertEqual(IP.objects.get().region_name, 'Ontario')
        self.assertEqual(IP.objects.get().city, 'Ottawa')
        self.assertEqual(IP.objects.get().latitude, Decimal('67.4289'))
        self.assertEqual(IP.objects.get().longitude, Decimal('-82.6844'))

    def test_create_ip_malformed(self):
        """
        Test malformed create data
        """
        url = reverse('ip-list')
        data = {'number': '174.114.57.163'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ip_detail(self):
        """
        Test IP detail endpoint
        """
        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'country_code': 'ca',
            'region_name': 'Ontario',
            'city': 'Ottawa',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip = IP(**data)
        ip.save()
        url = reverse('ip-detail', kwargs={'pk': ip.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], '174.114.57.161')
        self.assertEqual(response.data['country_name'], 'Canada')
        self.assertEqual(response.data['country_code'], 'ca')
        self.assertEqual(response.data['region_name'], 'Ontario')
        self.assertEqual(response.data['city'], 'Ottawa')
        self.assertEqual(response.data['latitude'], '67.4289')
        self.assertEqual(response.data['longitude'], '-82.6844')
        self.assertEqual(response.data['weather']['temperature'], 274.78)
        self.assertEqual(len(response.data['news']), 2)

    def test_ip_list(self):
        """
        Test IP list endpoint
        """
        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'country_code': 'ca',
            'region_name': 'Ontario',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip1 = IP(**data)
        ip1.save()

        data = {
            'number': '174.114.57.162',
            'country_name': 'Canada',
            'country_code': 'ca',
            'region_name': 'Ontario',
            'latitude': '60.7543',
            'longitude': '-90.6844'
        }
        ip2 = IP(**data)
        ip2.save()

        url = reverse('ip-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_404(self):
        url = reverse('ip-detail', kwargs={'pk': 333})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_ip_validation(self):
        """
        Test IP is valid
        """
        url = reverse('ip-list')
        data = {'number': '300.300.300.300'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

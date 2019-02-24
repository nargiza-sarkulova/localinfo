# -*- coding: utf-8 -*-
from decimal import Decimal
from mock import patch

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ip.models import IP
from clients.ipstack import IPstackAPIClient


class IPTest(TestCase):
    def test_ip_uniqueness(self):
        """
        Test IP number is unique accross table
        """
        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'region_name': 'Ontario',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip1 = IP(**data)
        ip1.save()

        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'region_name': 'Ontario',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip2 = IP(**data)
        self.assertRaises(IntegrityError, ip2.save)


def _mock_ip_info(self, ip_number):
    data = {'174.114.57.161': {'number': '174.114.57.161',
                               'country_name': 'Canada',
                               'region_name': 'Ontario',
                               'city': 'Ottawa',
                               'latitude': '67.4289',
                               'longitude': '-82.6844'},
            '174.114.57.162': {'number': '174.114.57.162',
                               'country_name': 'Canada',
                               'region_name': 'Ontario',
                               'latitude': '60.7543',
                               'longitude': '-90.6844'},
            '174.114.57.163': {'number': '174.114.57.162',
                               'country_name': 'Canada',
                               'region_name': 'Ontario',
                               'latitude': 'XXXX33',
                               'longitude': '-90.6844'}}
    return data.get(ip_number)


@patch.object(IPstackAPIClient, 'get_ip_info', _mock_ip_info)
class IpAPITest(APITestCase):

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
        self.assertEqual(response.data['region_name'], 'Ontario')
        self.assertEqual(response.data['city'], 'Ottawa')
        self.assertEqual(response.data['latitude'], '67.4289')
        self.assertEqual(response.data['longitude'], '-82.6844')

    def test_ip_list(self):
        """
        Test IP list endpoint
        """
        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'region_name': 'Ontario',
            'latitude': '67.4289',
            'longitude': '-82.6844'
        }
        ip1 = IP(**data)
        ip1.save()

        data = {
            'number': '174.114.57.162',
            'country_name': 'Canada',
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

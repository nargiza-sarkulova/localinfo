# -*- coding: utf-8 -*-
from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ip.models import IP


class IPTest(APITestCase):

    def test_create_ip(self):
        """
        Create new IP
        """
        url = reverse('ip-list')
        data = {
            'number': '174.114.57.161',
            'country_name': 'Canada',
            'region_name': 'Ontario',
            'city': 'Ottawa',
            'latitude': 67.4289,
            'longitude': -82.6844
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IP.objects.count(), 1)
        self.assertEqual(IP.objects.get().number, '174.114.57.161')
        self.assertEqual(IP.objects.get().country_name, 'Canada')
        self.assertEqual(IP.objects.get().region_name, 'Ontario')
        self.assertEqual(IP.objects.get().city, 'Ottawa')
        self.assertEqual(IP.objects.get().latitude, Decimal('67.4289'))
        self.assertEqual(IP.objects.get().longitude, Decimal('-82.6844'))

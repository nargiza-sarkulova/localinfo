# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ip.models import IP
from ip.serializers import IPSerializer
from ip.utils import is_ip_valid
from clients.ipstack import IPstackAPIClient
from clients.news import NewsAPIClient
from clients.open_weather import OpenWeatherAPIClient


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class BaseAPIView(APIView):
    """
    Base class for API views
    """
    def __init__(self, *args, **kwargs):
        super(BaseAPIView, self).__init__(*args, **kwargs)
        self.ip_client = IPstackAPIClient()
        self.news_client = NewsAPIClient()
        self.weather_client = OpenWeatherAPIClient()

    def get_additional_data(self, ip_info):
        weather = self.weather_client.get_weather_info(ip_info['latitude'], ip_info['longitude'])
        news = self.news_client.get_news(ip_info['country_code'])
        return {'weather': weather, 'news': news}

    def save_additional_data(self, ip_number, data):
        cache.set(ip_number, data, timeout=CACHE_TTL)

    def get_and_save_to_cache(self, ip_info):
        additional_data = self.get_additional_data(ip_info)
        self.save_additional_data(ip_info['number'], additional_data)
        return additional_data

    def get_or_save_to_cache(self, ip_info):
        ip_number = ip_info['number']
        if ip_number in cache:
            additional_data = cache.get(ip_number)  # retrieve from cache if exists
        else:
            additional_data = self.get_and_save_to_cache(ip_info)  # fetch if doesn't exist
        return {**ip_info, **additional_data}


class IPList(BaseAPIView):
    """
    List all saved IPs
    """
    def get_object(self, ip_number):
        try:
            return IP.objects.get(number=ip_number)
        except IP.DoesNotExist:
            return False

    def get(self, request):
        ips = IP.objects.all()
        serializer = IPSerializer(ips, many=True)
        return Response(serializer.data)

    def post(self, request):
        ip_number = request.data['number']
        if not is_ip_valid(ip_number):
            return Response('{"number":["A valid IP number is required."]}',
                            status=status.HTTP_400_BAD_REQUEST)
        ip = self.get_object(ip_number)
        if ip:
            # if IP object already exists serve data from cache if possible
            ip_info = IPSerializer(ip).data
            return Response(self.get_or_save_to_cache(ip_info))
        # if IP is new fetch data from external APIs and save to cache
        ip_info = self.ip_client.get_ip_info(ip_number)
        serializer = IPSerializer(data=ip_info)
        if serializer.is_valid():
            serializer.save()
            additional_data = self.get_and_save_to_cache(ip_info)
            return Response({**serializer.data, **additional_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IPDetail(BaseAPIView):
    """
    Retrieve a saved IP
    """
    def get_object(self, pk):
        try:
            return IP.objects.get(pk=pk)
        except IP.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        serializer = IPSerializer(self.get_object(pk))
        # if IP object exists but weather and news data has expired re-fetch and save to cache
        result = self.get_or_save_to_cache(serializer.data)
        return Response(result)

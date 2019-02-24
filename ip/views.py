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
from clients.open_weather import OpenWeatherAPIClient


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class IPList(APIView):
    """
    List all saved IPs.
    """
    def __init__(self, *args, **kwargs):
        super(IPList, self).__init__(*args, **kwargs)
        self.ip_client = IPstackAPIClient()
        self.weather_client = OpenWeatherAPIClient()

    def save_data_in_cache(self, ip_info):
        weather = self.weather_client.get_weather_info(ip_info['latitude'], ip_info['longitude'])
        data = {'weather': weather}
        cache.set(ip_info['number'], data, timeout=CACHE_TTL)

    def get(self, request):
        ips = IP.objects.all()
        serializer = IPSerializer(ips, many=True)
        return Response(serializer.data)

    def post(self, request):
        ip_number = request.data['number']
        if not is_ip_valid(ip_number):
            return Response('{"number":["A valid IP number is required."]}',
                            status=status.HTTP_400_BAD_REQUEST)
        ip_info = self.ip_client.get_ip_info(ip_number)
        serializer = IPSerializer(data=ip_info)
        if serializer.is_valid():
            serializer.save()
            self.save_data_in_cache(ip_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IPDetail(APIView):
    """
    Retrieve a saved IP.
    """
    def get_object(self, pk):
        try:
            return IP.objects.get(pk=pk)
        except IP.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ip = self.get_object(pk)
        serializer = IPSerializer(ip)
        result = serializer.data
        if ip.number in cache:
            data = cache.get(ip.number)
            result = {**serializer.data, **data}
        return Response(result)
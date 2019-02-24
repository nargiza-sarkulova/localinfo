# -*- coding: utf-8 -*-
from rest_framework import serializers

from ip.models import IP


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ('id', 'number', 'country_name', 'country_flag', 'region_name', 'city',
                  'latitude', 'longitude')

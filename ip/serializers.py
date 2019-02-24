# -*- coding: utf-8 -*-
from rest_framework import serializers

from ip.models import IP
from ip.utils import is_ip_valid


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ('id', 'number', 'country_name', 'country_code', 'country_flag', 'region_name',
                  'city', 'latitude', 'longitude')

    def validate_number(self, value):
        """
        Validate IP number.
        """
        if not is_ip_valid(value):
            raise serializers.ValidationError("IP number should be valid")
        return value

# -*- coding: utf-8 -*-
from IPy import IP as ip_validate

from rest_framework import serializers

from ip.models import IP


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ('id', 'number', 'country_name', 'country_flag', 'region_name', 'city',
                  'latitude', 'longitude')

    def validate_number(self, value):
        """
        Validate IP number.
        """
        try:
            ip_validate(value)
        except ValueError:
            raise serializers.ValidationError("IP number should be valid")
        return value

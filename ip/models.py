# -*- coding: utf-8 -*-
from django.db import models


class IP(models.Model):
    number = models.CharField(max_length=15, unique=True)
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    country_flag = models.CharField(max_length=100, blank=True)
    region_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)

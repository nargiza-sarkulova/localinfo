# -*- coding: utf-8 -*-
from django.urls import path

from ip import views


urlpatterns = [
    path('ips/', views.IPList.as_view(), name='ip-list'),
    path('ips/<int:pk>/', views.IPDetail.as_view(), name='ip-detail'),
]

# -*- coding: utf-8 -*-
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ip.models import IP
from ip.serializers import IPSerializer


class IPList(APIView):
    """
    List all saved IPs.
    """
    def get(self, request):
        ips = IP.objects.all()
        serializer = IPSerializer(ips, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        return Response(serializer.data)

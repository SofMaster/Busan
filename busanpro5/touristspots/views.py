import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import  permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from knox.auth import TokenAuthentication

from .models import TouristSpot, FavoriteSpot, RecommendModel
from .serializers import TouristSpotSerializer, FavoriteSpotSerializer
from django.db.models import Q

class TouristSpotsList(generics.ListCreateAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer

class TouristSpotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer


class MyFavoriteSpotsList(generics.ListCreateAPIView):
    queryset = FavoriteSpot.objects.all()
    serializer_class = FavoriteSpotSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(user=self.request.user)
        serializer = FavoriteSpotSerializer(queryset, many=True)
        return Response(serializer.data)

class MyFavoriteSpotsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavoriteSpot.objects.all()
    serializer_class = FavoriteSpotSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


from .recommendspots import recommed
import pandas as pd

class RecommendList(APIView):

    def get(self, request, format=None):
        theme = request.GET.get('theme', '')
        companion = request.GET.get('companion', '')
        age = request.GET.get('age', '')
	    # query = request.GET.get('query', 'price')

        a = recommed(theme, companion, age)
        arr = a.tolist()
        spots = TouristSpot.objects.filter(Q(name=arr[0]) | Q(name=arr[1]) | Q(name=arr[2]))

        serializer = TouristSpotSerializer(spots, many=True)
        return Response(serializer.data)



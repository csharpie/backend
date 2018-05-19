from django.db.models import Count
from api.models import Location
from api.models import Category
from api.models import Hour
from api.serializers import LocationSerializer, HourSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = Location.objects.all()
        return queryset


class NearbyLocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        # Radius in meters
        radius = self.request.query_params.get('radius', 1000)
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')

        # set default map center if no params are passed in
        if not (lat and lon):
            lat = 39.95233
            lon = -75.16379

        queryset = Location.objects.in_distance(int(radius), fields=['latitude', 'longitude'],
                                                points=[float(lat), float(lon)])

        return queryset


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CommunityGardenLocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter(category=1)


class GroceryStoreLocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter(category=2)


class FoodPantryLocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter(category=3)


class SuperMarketLocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter(category=4)


class HourList(generics.ListCreateAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer


class HourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer


class AnalyticsLocationSummary(APIView):
    renderer_class = (JSONRenderer,)
    serializer_class = LocationSerializer

    def get(self, request, format=None):
        return Response({'total locations': Location.objects.all().count()})


class AnalyticsLocationSummaryCategory(APIView):
    renderer_class = (JSONRenderer,)
    
    def get(self, request, format=None):
        content = Category.objects.values('name')\
                .annotate(total_locations=Count('location'))
        return Response(content)

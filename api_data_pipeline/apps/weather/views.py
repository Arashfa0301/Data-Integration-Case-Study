from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import requests
import pandas as pd


from api_data_pipeline.apps.weather.models import Weather, Location
from api_data_pipeline.apps.weather.serializers import WeatherSerializer
from api_data_pipeline.apps.weather.constants import OpenWeather_URLS
import moment


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    @action(detail=False, methods=["GET"])
    def load_city_weather(self, request):
        city = self.request.query_params.get("city")

        langLatResponse = requests.get(
            OpenWeather_URLS.get_coordinates_by_city(city=city)
        ).json()[0]
        latitude = langLatResponse["lat"]
        longitude = langLatResponse["lon"]

        weatherResponse = requests.get(
            OpenWeather_URLS.get_get_weather_by_coordinates(lat=latitude, lon=longitude)
        ).json()

        location = Location.objects.get_or_create(
            city=city, latitude=latitude, longitude=longitude
        )

        date = moment.unix(weatherResponse["dt"])
        # Weather.objects.create(location=location, date=ti)
        print(date)
        print(weatherResponse["weather"])
        return JsonResponse(weatherResponse)

    @action(detail=False, methods=["GET"])
    def get_all_weathers_by_city(self, request):
        city = self.request.query_params.get("city")
        if not city:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            weatherObjects = Weather.objects.get(city=city)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(
            WeatherSerializer(
                weatherObjects,
                many=True,
            ).data
        )

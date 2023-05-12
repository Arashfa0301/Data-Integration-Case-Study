from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
import requests
import pandas as pd
import datetime


from api_data_pipeline.apps.weather.models import Weather, Location
from api_data_pipeline.apps.weather.serializers import WeatherSerializer
from api_data_pipeline.apps.weather.constants import OpenWeather_URLS
import moment


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    def load_current_weather(self, city):
        langLatResponse = requests.get(
            OpenWeather_URLS.get_coordinates_by_city(city=city)
        ).json()[0]
        latitude, longitude = langLatResponse["lat"], langLatResponse["lon"]

        weatherResponse = requests.get(
            OpenWeather_URLS.get_weather_by_coordinates(lat=latitude, lon=longitude)
        ).json()
        weatherDF = pd.json_normalize(weatherResponse)
        location = Location.objects.get_or_create(
            city=city, latitude=latitude, longitude=longitude
        )[0]
        wDate = moment.unix(weatherResponse["dt"])

        try:
            currentWeather = Weather.objects.create(
                location=location,
                date=datetime.date(wDate.year, wDate.month, wDate.day),
                weather_condition=weatherDF.loc[0, "weather"][0]["main"],
                weather_description=weatherDF.loc[0, "weather"][0]["description"],
                temperature=weatherDF.loc[0, "main.temp"],
                pressure=weatherDF.loc[0, "main.pressure"],
                humidity=weatherDF.loc[0, "main.humidity"],
                wind_speed=weatherDF.loc[0, "wind.speed"],
            )
        except IntegrityError:
            currentWeather = Weather.objects.get(
                location=location,
                date=datetime.date(wDate.year, wDate.month, wDate.day),
            )

        return currentWeather

    @action(detail=False, methods=["GET"])
    def load_current_weather_by_city(self, request):
        city = self.request.query_params.get("city")
        if not city:
            return Response(
                {"Fail": "The city was not specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        currentWeather = self.load_current_weather(city)

        return Response(
            WeatherSerializer(
                currentWeather,
            ).data
        )

    @action(detail=False, methods=["GET"])
    def get_all_weathers(self, request):
        city = self.request.query_params.get("city")
        if not city:
            return Response(
                WeatherSerializer(
                    Weather.objects.all(),
                    many=True,
                ).data
            )

        location = (
            self.load_current_weather(city).location
            if Weather.objects.filter(location__city=city).exists()
            else Location.objects.get(city=city)
        )

        return Response(
            WeatherSerializer(
                Weather.objects.filter(location=location),
                many=True,
            ).data
        )

    @action(detail=False, methods=["GET"])
    def clear_weather_database(self, request):
        Weather.objects.all().delete()
        return Response(status=status.HTTP_200_OK)

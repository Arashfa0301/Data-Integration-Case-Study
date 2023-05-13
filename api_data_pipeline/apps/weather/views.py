from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
import requests
import pandas as pd
import datetime


from api_data_pipeline.apps.weather.models import Weather, Location
from api_data_pipeline.apps.weather.serializers import (
    WeatherSerializer,
    LocationSerializer,
)
from api_data_pipeline.apps.weather.constants import OpenWeather_URLS
import moment


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    @action(detail=False, methods=["GET"])
    def load_current_weather_by_city(self, request) -> Response:
        city = self.request.query_params.get("city")
        if not city:
            return Response(
                {"Fail": "The city was not specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        currentWeather = self.load_current_weather(city)
        print(Weather.objects.all().count())

        return Response(
            WeatherSerializer(
                currentWeather,
            ).data
        )

    @action(detail=False, methods=["GET"])
    def get_all_weathers(self, request) -> Response:
        city = self.request.query_params.get("city")
        if not city:
            return Response(
                WeatherSerializer(
                    Weather.objects.all(),
                    many=True,
                ).data
            )

        location = (
            Location.objects.get(city=city)
            if Weather.objects.filter(location__city=city).exists()
            else self.load_current_weather(city).location
        )

        return Response(
            WeatherSerializer(
                Weather.objects.filter(location=location),
                many=True,
            ).data
        )

    @action(detail=False, methods=["GET"])
    def get_forecast_for_5_days_for_city(self, request) -> Response:
        city = self.request.query_params.get("city")
        if not city:
            return Response(
                {"Fail": "The city was not specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location = (
            Location.objects.get(city=city)
            if Weather.objects.filter(location__city=city).exists()
            else self.create_location(city)
        )
        print(Location.objects.all().count())

        self.load_forecast_for_5_days_for_city(location)
        return Response(
            WeatherSerializer(
                Weather.objects.filter(location=location),
                many=True,
            ).data
        )

    @action(detail=False, methods=["GET"])
    def clear_weather_database(self, request) -> Response:
        Weather.objects.all().delete()
        Location.objects.all().delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_all_loaded_locations(self, request) -> Response:
        for i in range(100):
            latLonResponse = requests.get(
                OpenWeather_URLS.get_coordinates_by_city(city="London")
            ).json()[0]

        return Response(
            LocationSerializer(
                Location.objects.all(),
                many=True,
            ).data
        )

    def load_current_weather(self, city: str) -> Weather:
        latLonResponse = requests.get(
            OpenWeather_URLS.get_coordinates_by_city(city=city)
        ).json()[0]
        latitude, longitude = latLonResponse["lat"], latLonResponse["lon"]

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

    def load_forecast_for_5_days_for_city(self, location: Location) -> None:
        latitude, longitude = location.latitude, location.longitude

        weathersResponse = requests.get(
            OpenWeather_URLS.get_weather_forcast_for_five_days_by_coordinates(
                lat=latitude, lon=longitude
            )
        ).json()["list"]

        for weatherJson in weathersResponse:
            weatherDF = pd.json_normalize(weatherJson)
            wDate = moment.unix(weatherJson["dt"])
            try:
                Weather.objects.create(
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
                continue

    def create_location(self, city: str) -> Location:
        latLonResponse = requests.get(
            OpenWeather_URLS.get_coordinates_by_city(city=city)
        ).json()[0]
        latitude, longitude = latLonResponse["lat"], latLonResponse["lon"]

        return Location.objects.create(
            city=city, latitude=latitude, longitude=longitude
        )

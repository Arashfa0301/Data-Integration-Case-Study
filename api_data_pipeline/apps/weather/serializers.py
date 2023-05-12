from rest_framework import serializers

from api_data_pipeline.apps.weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = [
            "location",
            "date",
            "weather_condition",
            "weather_description",
            "temperature",
            "pressure",
            "humidity",
            "wind_speed",
        ]

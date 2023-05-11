from rest_framework import serializers

from api_data_pipeline.apps.weather.models import Weather


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather
        fields = ["__all__"]

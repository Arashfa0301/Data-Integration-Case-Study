from django.db import models

# from django.contrib.gis.db import models

from django.utils import timezone
from api_data_pipeline.apps.weather.constants import WEATHER_CONDITION_CHOICES


class Location(models.Model):
    city = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["city", "latitude", "longitude"],
                name="unique_city_coordinates_combination",
            )
        ]


class Weather(models.Model):
    location = models.ForeignKey(
        Location, related_name="weathers", on_delete=models.CASCADE
    )
    date = models.DateField(default=timezone.now)
    weather_condition = models.CharField(
        max_length=100, choices=WEATHER_CONDITION_CHOICES
    )
    weather_description = models.CharField(max_length=100, null=True)
    temperature = models.FloatField()
    wind_speed = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["location", "date"], name="unique_location_date_combination"
            )
        ]

    def __str__(self) -> str:
        return f"location: {self.location}, date: {self.date}, weather_condition: {self.weather_condition}, temperature: {self.temperature}"

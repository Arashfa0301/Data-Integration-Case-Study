"""
URL configuration for api_data_pipeline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.contrib import admin
from api_data_pipeline.types import URLList
from django.urls import path, include, re_path
from api_data_pipeline.apps.news.views import NewsViewSet
from api_data_pipeline.apps.weather.views import WeatherViewSet


routers = routers.DefaultRouter()
routers.register(r"news", NewsViewSet, basename="news")
routers.register(r"weather", WeatherViewSet, basename="weather")

# base urls
urlpatterns: URLList = [
    path("", include(routers.urls)),
    path("admin/", admin.site.urls),
]

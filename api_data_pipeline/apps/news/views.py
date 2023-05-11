from rest_framework import viewsets, decorators
from rest_framework.decorators import action
from django.shortcuts import render
from django.http import HttpResponse

# import requests
import pandas as pd


from api_data_pipeline.apps.news.models import Article
from api_data_pipeline.apps.news.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = NewsSerializer

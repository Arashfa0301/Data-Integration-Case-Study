from django.db import models
from api_data_pipeline.apps.news.constants import (
    NEWS_CATEGORY_CHOICES,
    NEWS_COUNTRY_CHOICES,
    NEWS_LANGUAGE_CHOICES,
)


class Source(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=NEWS_CATEGORY_CHOICES)
    language = models.CharField(max_length=5, choices=NEWS_LANGUAGE_CHOICES)
    country = models.CharField(max_length=5, choices=NEWS_COUNTRY_CHOICES)


class Article(models.Model):
    source = models.ForeignKey(
        Source, related_name="articles", on_delete=models.CASCADE
    )
    author = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True)
    published_at = models.DateField()
    content = models.CharField(max_length=1000)
    top_headline = models.BooleanField(default=False)

    @property
    def category(self):
        return self.source.category

from django.db import models


class Article(models.Model):
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    urlToImage = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    publishedAt = models.DateField()

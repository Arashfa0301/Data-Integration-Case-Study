from rest_framework import serializers

from api_data_pipeline.apps.news.models import Article, Source


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "source",
            "title",
            "category",
            "author",
            "description",
            "url",
            "published_at",
            "content",
        ]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = [
            "name",
            "description",
            "url",
            "category",
            "language",
            "country",
        ]

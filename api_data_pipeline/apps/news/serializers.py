from rest_framework import serializers

from api_data_pipeline.apps.news.models import Article


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ["__all__"]

import datetime
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
import requests
from django.db import IntegrityError
import pandas as pd
from api_data_pipeline.apps.news.constants import (
    NEWS_CATEGORY_CHOICES,
    NEWS_COUNTRY_CHOICES,
    NEWS_LANGUAGE_CHOICES,
    NEWSAPI_URLS,
)
from api_data_pipeline.apps.news.models import Article, Source
from api_data_pipeline.apps.news.serializers import SourceSerializer, ArticleSerializer
import moment as moment


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @action(detail=False, methods=["GET"])
    def get_top_headlines_today_by_country(self, request) -> Response:
        self.load_all_top_sources()

        country = self.request.query_params.get("country")
        if not country in self.choices_to_list(NEWS_COUNTRY_CHOICES):
            return self.return_invalid_choice_response("country")

        responseJson = requests.get(NEWSAPI_URLS.get_top_headlines(country)).json()
        if self.check_rate_limited(responseJson):
            return Response(
                {"Error": "API rate limit reached"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        articlesJson = responseJson["articles"]

        self.load_headlines_from_json(articlesJson)

        return Response(
            ArticleSerializer(
                Article.objects.filter(top_headline=True, source__country=country),
                many=True,
            ).data
        )

    @action(detail=False, methods=["GET"])
    def load_articles_of_the_last_thirdy_days(self, request) -> Response:
        source = self.request.query_params.get("source")

        if not source or not Source.objects.filter(name=source).exists():
            return self.return_invalid_choice_response("source")

        responseJson = requests.get(NEWSAPI_URLS.get_everything(source)).json()
        if self.check_rate_limited(responseJson):
            return Response(
                {"Error": "API rate limit reached"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        articlesJson = responseJson["articles"]

        self.load_headlines_from_json(articlesJson)

        return Response(ArticleSerializer(Article.objects.all(), many=True).data)

    @action(detail=False, methods=["GET"])
    def get_articles_by_date_of_the_last_thirdy_days(self, request) -> Response:
        self.load_all_top_sources()

        # Check if the source is valid
        source = self.request.query_params.get("source")
        if not source or not Source.objects.filter(name=source).exists():
            return self.return_invalid_choice_response("source")

        # Check if the date is valid
        date = self.request.query_params.get("date")
        if not date or not (
            (timezone.now() - datetime.timedelta(days=30)).date()
            < datetime.date(*[int(x) for x in date.split("-")])
            < timezone.now().date()
        ):
            return self.return_invalid_choice_response("date")

        date = datetime.date(*[int(x) for x in date.split("-")])
        responseJson = requests.get(NEWSAPI_URLS.get_everything(source, date)).json()
        if self.check_rate_limited(responseJson):
            return Response(
                {"Error": "API rate limit reached"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        articlesJson = responseJson["articles"]
        self.load_headlines_from_json(articlesJson)

        return Response(
            ArticleSerializer(Article.objects.filter(published_at=date), many=True).data
        )

    @action(detail=False, methods=["GET"])
    def get_sources(self, request) -> Response:
        """Loads and returns all the sources"""
        if self.load_all_top_sources() == False:
            return Response(
                {"Error": "API rate limit reached"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        category = self.request.query_params.get("category")
        language = self.request.query_params.get("language")
        country = self.request.query_params.get("country")
        sources = Source.objects.all()
        # Check if the category is valid
        if category:
            if not category in self.choices_to_list(NEWS_CATEGORY_CHOICES):
                return self.return_invalid_choice_response("category")
            sources = sources.filter(category=category)
        # Check if the language is valid
        if language:
            if not language in self.choices_to_list(NEWS_LANGUAGE_CHOICES):
                return self.return_invalid_choice_response("language")
            sources = sources.filter(language=language)
        # Check if the country is valid
        if country:
            if not country in self.choices_to_list(NEWS_COUNTRY_CHOICES):
                return self.return_invalid_choice_response("country")
            sources = sources.filter(country=country)

        return Response(SourceSerializer(sources, many=True).data)

    @action(detail=False, methods=["GET"])
    def clear_db(self, request) -> Response:
        """Clears the database of all instances of Sources and Articles"""
        Source.objects.all().delete()
        Article.objects.all().delete()
        return Response(
            {"Success": "Succesfully deleted all instances of Sources and Articles"},
            status=status.HTTP_200_OK,
        )

    def choices_to_list(self, choices) -> list:
        return [choice[0] for choice in choices]

    def return_invalid_choice_response(self, choice) -> Response:
        return Response(
            {"Fail": f"The {choice} specified is not valid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def load_all_top_sources(self) -> bool | None:
        responseJson = requests.get(NEWSAPI_URLS.get_top_sources()).json()
        if self.check_rate_limited(responseJson):
            return False
        sourcesJson = responseJson["sources"]

        for source in sourcesJson:
            Source.objects.get_or_create(
                name=source["name"],
                description=source["description"],
                url=source["url"],
                category=source["category"],
                language=source["language"],
                country=source["country"],
            )

    def load_headlines_from_json(self, articlesJson: list) -> None:
        for article in articlesJson:
            published_at = moment.date(article["publishedAt"])
            source = Source.objects.get_or_create(name=article["source"]["name"])

            try:
                Article.objects.create(
                    source=source[0],
                    author=article["author"],
                    title=article["title"],
                    description=article["description"],
                    url=article["url"],
                    published_at=datetime.date(
                        published_at.year, published_at.month, published_at.day
                    ),
                    content=article["content"],
                    top_headline=True,
                )
            except IntegrityError:
                continue

    def check_rate_limited(self, responseJson: dict) -> bool:
        if responseJson["status"] == "error":
            return responseJson["code"] == "rateLimited"

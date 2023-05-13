from datetime import timedelta
from django.utils import timezone

from api_data_pipeline.apps.constants import API_KEYS


class NEWSAPI_URLS:
    def get_top_headlines(country, q="", category="", source="") -> str:
        return f"https://newsapi.org/v2/top-headlines?country={country}&q={q}&category={category}&sources={source}&apiKey={API_KEYS.NEWSAPI_URL}"

    def get_top_sources() -> str:
        return f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEYS.NEWSAPI_URL}"

    def get_everything(sources, date=timezone.now() - timedelta(days=30), q="") -> str:
        return f"https://newsapi.org/v2/everything?sources={sources}&q={q}&from={date}&sortBy=popularity&apiKey={API_KEYS.NEWSAPI_URL}"


NEWS_CATEGORY_CHOICES = [
    ("business", "business"),
    ("entertainment", "entertainment"),
    ("general", "general"),
    ("health", "health"),
    ("science", "science"),
    ("sports", "sports"),
    ("technology", "technology"),
]

NEWS_LANGUAGE_CHOICES = [
    ("ar", "ar"),
    ("de", "de"),
    ("en", "en"),
    ("es", "es"),
    ("fr", "fr"),
    ("he", "he"),
    ("it", "it"),
    ("nl", "nl"),
    ("no", "no"),
    ("pt", "pt"),
    ("ru", "ru"),
    ("sv", "sv"),
    ("ud", "ud"),
    ("zh", "zh"),
]

NEWS_COUNTRY_CHOICES = [
    ("ae", "ae"),
    ("ar", "ar"),
    ("at", "at"),
    ("au", "au"),
    ("be", "be"),
    ("bg", "bg"),
    ("br", "br"),
    ("ca", "ca"),
    ("ch", "ch"),
    ("cn", "cn"),
    ("co", "co"),
    ("cu", "cu"),
    ("cz", "cz"),
    ("de", "de"),
    ("eg", "eg"),
    ("fr", "fr"),
    ("gb", "gb"),
    ("gr", "gr"),
    ("hk", "hk"),
    ("hu", "hu"),
    ("id", "id"),
    ("ie", "ie"),
    ("il", "il"),
    ("in", "in"),
    ("it", "it"),
    ("jp", "jp"),
    ("kr", "kr"),
    ("lt", "lt"),
    ("lv", "lv"),
    ("ma", "ma"),
    ("mx", "mx"),
    ("my", "my"),
    ("ng", "ng"),
    ("nl", "nl"),
    ("no", "no"),
    ("nz", "nz"),
    ("ph", "ph"),
    ("pl", "pl"),
    ("pt", "pt"),
    ("ro", "ro"),
    ("rs", "rs"),
    ("ru", "ru"),
    ("sa", "sa"),
    ("se", "se"),
    ("sg", "sg"),
    ("si", "si"),
    ("sk", "sk"),
    ("th", "th"),
    ("tr", "tr"),
    ("tw", "tw"),
    ("ua", "ua"),
    ("us", "us"),
    ("ve", "ve"),
    ("za", "za"),
]


NEWS_SORTBY_CHOICES = [
    ("relevancy", "relevancy"),
    ("popularity", "popularity"),
    ("publishedAt", "publishedAt"),
]

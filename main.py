import pandas as pd
import requests as requests


news = requests.get(
    "https://newsapi.org/v2/top-headlines?country=us&apiKey=67f31dfa787f434a8916dc9bc96ff745"
)
newsJson = news.json()
pandasNews = pd.DataFrame(newsJson["articles"][0])
print(pandasNews.columns)


weather = requests.get(
    "https://api.openweathermap.org/data/2.5/weather?lat=59.946758&lon=10.789349&appid=6119f4e8774c05271075aa5fb9764ea6"
)
weatherJson = weather.json()
pandasWeather = pd.DataFrame.from_dict(weatherJson)
print(weatherJson)

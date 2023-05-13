# Python-based Pipeline for Integrating OpenWeatherMap and NewsAPI Data

This project is a Python-based pipeline that integrates data from two public APIs (OpenWeatherMap and NewsAPI) using open-source technologies. The pipeline also provides a REST API endpoint that can query the integrated data and return the results in a JSON format.

## Requirements

To run this pipeline, you will need the following:

- Python 3.7 or later
- Access to the OpenWeatherMap API (https://openweathermap.org/api)
- Access to the NewsAPI (https://newsapi.org/)
- [Docker](https://docs.docker.com/get-docker/)

## Usage

To run the pipeline, do the following:

1. Clone the repository: `git@github.com:Arashfa0301/Data-Integration-Case-Study.git`
2. Set your API keys for OpenWeatherMap and NewsAPI in the `api_data_pipeline/apps/constants.py` file.
3. Run via docker

```bash
$ docker compose up --build
```

## Sample APIs

### Articles of the last 30 days

_Example:_

```shell
http://localhost:8000/news/load_articles_of_the_last_thirdy_days?source=Aftenposten
```

_Result:_

```json
[{
		"source": "Aftenposten",
		"title": "Byrådet bekymret for «hytteleiligheter». Vil utrede boplikt i Oslo.",
		"category": "general",
		"author": null,
		"url": "https://www.aftenposten.no/oslo/i/BWmgEl/byraadet-bekymret-for-hytteleiligheter-vil-utrede-boplikt-i-oslo",
		"published_at": "2023-04-18",
		"content": "Byrådet frykter at fritidsboliger er i ferd med å bli et problem for boligmarkedet i Oslo. Nå åpner de for å innføre boplikt i hovedstaden.\r\nHytte i byen? Det vil stadig flere ha, ifølge meglere. Byr… [+4444 chars]"
	},
  ...
]
```

### Get all publishing sources

_Example:_

```shell
http://localhost:8000/news/get_sources/
```

_Result:_

```json
[
  {
		"name": "ABC News",
		"description": "Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos at ABCNews.com.",
		"url": "https://abcnews.go.com",
		"category": "general",
		"language": "en",
		"country": "us"
	},
	{
		"name": "ABC News (AU)",
		"description": "Australia's most trusted source of local, national and world news. Comprehensive, independent, in-depth analysis, the latest business, sport, weather and more.",
		"url": "http://www.abc.net.au/news",
		"category": "general",
		"language": "en",
		"country": "au"
	},
  ...
]
```

### Get city forecast for the incoming 5 days

_Example:_

```shell
http://localhost:8000/weather/get_forecast_for_5_days_for_city/?city=Bergen
```

_Result:_

```json
[
  {
		"location": "Bergen",
		"date": "2023-05-13",
		"weather_condition": "Clear",
		"weather_description": "clear sky",
		"temperature": 282.66,
		"pressure": 1024.0,
		"humidity": 94.0,
		"wind_speed": 3.6
	},
      ...
  ,
	{
		"location": "Bergen",
		"date": "2023-05-18",
		"weather_condition": "Clouds",
		"weather_description": "few clouds",
		"temperature": 277.41,
		"pressure": 1025.0,
		"humidity": 76.0,
		"wind_speed": 1.68
	}
]
```

### Other APIs

```shell
http://localhost:8000/weather/load_current_weather_by_city/?city={city}
```

```shell
http://localhost:8000/weather/get_all_weathers/?city={city}
```

```shell
http://localhost:8000/weather/clear_weather_database
```

```shell
http://localhost:8000/weather/get_all_loaded_locations
```

```shell
http://localhost:8000/news/get_top_headlines_today_by_country?country={country}
```

```shell
http://localhost:8000/news/get_articles_by_date_of_the_last_thirdy_days?source={source}&date={YYYY-MM-DD}
```

```shell
http://localhost:8000/news/get_sources?category={category}&language={language}&country={country}
```

```shell
http://localhost:8000/news/clear_db
```

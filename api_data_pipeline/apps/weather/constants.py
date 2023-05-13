from api_data_pipeline.apps.constants import API_KEYS


class OpenWeather_URLS:
    def get_coordinates_by_city(city):
        return f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEYS.OPENWEATHER_URL}"

    def get_weather_by_coordinates(lat, lon):
        return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEYS.OPENWEATHER_URL}"

    def get_weather_forcast_for_five_days_by_coordinates(lat, lon):
        return f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEYS.OPENWEATHER_URL}"


class UTIL_URLS:
    def get_county_code_by_name_json():
        return "https://pkgstore.datahub.io/core/country-list/data_json/data/8c458f2d15d9f2119654b29ede6e45b8/data_json.jsonv"


WEATHER_CONDITION_CHOICES = [
    ("Thunderstorm", "Thunderstorm"),
    ("Drizzle", "Drizzle"),
    ("Rain", "Rain"),
    ("Snow", "Snow"),
    ("Mist", "Mist"),
    ("Smoke", "Smoke"),
    ("Haze", "Haze"),
    ("Dust", "Dust"),
    ("Fog", "Fog"),
    ("Sand", "Sand"),
    ("Dust", "Dust"),
    ("Ash", "Ash"),
    ("Squall", "Squall"),
    ("Tornado", "Tornado"),
    ("Clear", "Clear"),
    ("Clouds", "Clouds"),
]

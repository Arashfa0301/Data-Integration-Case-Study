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


class OpenWeather_URLS:
    def get_coordinates_by_city(city):
        return f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=6119f4e8774c05271075aa5fb9764ea6"

    def get_weather_by_coordinates(lat, lon):
        return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=6119f4e8774c05271075aa5fb9764ea6"

    def get_weather_forcast_for_five_days_by_coordinates(lat, lon):
        return f"api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=6119f4e8774c05271075aa5fb9764ea6"

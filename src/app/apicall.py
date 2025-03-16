import requests


class OpenWeatherClient:
    curr_weather_api_url_string = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"
    city_coords = None

    def __init__(self,city_coords):
        self.city_coords = city_coords

    def get_current_weather(self, city: str, api_key: str):
        url = self.curr_weather_api_url_string.format(lat = self.city_coords[city][0], lon = self.city_coords[city][1], key = api_key)
        rs = requests.get(url)

        try:
            data = rs.json()
        except requests.JSONDecodeError:
            data = None

        return (data)

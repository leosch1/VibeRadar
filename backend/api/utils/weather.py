from openmeteo_requests import Client
from random import choice
from typing import Literal


class Weather:
    def __init__(self):
        self.client = Client()
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            "latitude": None,
            "longitude": None,
            "current": ["temperature_2m", "weather_code"],
            "timezone": "auto",
            "past_days": 0,
            "forecast_days": 1,
        }

    def get_from_coords(self, lat: float, lng: float) -> dict:
        """
        Get current weather data from Open Meteo API with given latitude and longitude.

        Args:
            lat (float): Latitude of the location.
            lng (float): Longitude of the location.
        
        Returns:
            dict: A dictionary containing the current temperature in Celsius and weather type.
        """
        # Set the latitude and longitude in the parameters
        self.params["latitude"] = lat
        self.params["longitude"] = lng

        # Make the API request
        response = self.client.weather_api(self.url, self.params)
        
        response = response[0]

        # Get the timeoffset in seconds to UTC
        utc_offset_seconds = response.UtcOffsetSeconds()
    
        # Extract current weather data
        weather = response.Current()
        temperature_2m = weather.Variables(0).Value()
        weather_code = weather.Variables(1).Value()

        # Round the temperature and convert wheather code to descriptive type
        temperature_celsius = round(temperature_2m, 0)
        weather_type = self._weather_code_to_type(weather_code)

        return {
            "utcOffsetSeconds": utc_offset_seconds,
            "weather": {
                "temperatureCelsius": temperature_celsius,
                "type": weather_type,
            }
        }

    @staticmethod    
    def _weather_code_to_type(code: int) -> Literal["cloudy", "sunny", "rainy", "snowy"]:
        """
        Convert Open Meteo weather codes to descriptive weather types.
        
        Args:
            code (int): Open Meteo weather code.
            
        Returns:
            Literal["cloudy", "sunny", "rainy", "snowy"]: Descriptive weather type.
        """
        if code in [0, 1]:
            return "sunny"
        elif code in [2, 3, 45, 48]:
            return "cloudy"
        elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
            return "rainy"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "snowy"
        else:
            return "sunny"
        

if __name__ == "__main__":
    # Example usage
    weather = Weather()
    lat = 47.665813
    lng = 8.426616
    weather_data = weather.get_from_coords(lat, lng)
    print(weather_data)
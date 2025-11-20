import httpx
import logging
from typing import Optional

logger = logging.getLogger("planner_app")


class OpenWeatherMapAPI:
    """Клієнт для взаємодії з OpenWeatherMap API."""
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str, city: str):
        self.api_key = api_key
        self.city = city

    def _map_weather_code(self, code: int, description: str) -> str:
        """Перетворює код OpenWeatherMap в одну з наших стратегій (Sunny, Rainy, Snowy, Cloudy)."""
        if 200 <= code < 300 or 500 <= code < 600:  # Thunderstorm, Rain
            return "Rainy"
        elif 600 <= code < 700:  # Snow
            return "Snowy"
        elif 700 <= code < 800:  # Atmosphere (Mist, Fog, etc.)
            return "Cloudy"
        elif code == 800:  # Clear
            return "Sunny"
        elif 801 <= code < 900:  # Clouds
            return "Cloudy"
        return "Cloudy"  # За замовчуванням

    async def fetch_weather_data(self) -> Optional[dict]:
        """Виконує запит до OpenWeatherMap."""
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric"  # Температура в Цельсіях
        }

        if not self.api_key:
            logger.error("OPENWEATHER_API_KEY is missing. Cannot fetch weather.")
            return None

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()  # Підніме виняток для 4xx/5xx помилок
                data = response.json()

                weather_main = data["weather"][0]

                result = {
                    "location": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": weather_main["description"],
                    "condition": self._map_weather_code(weather_main["id"], weather_main["description"]),
                }
                logger.info(f"[API] Weather data fetched: {result['condition']}, {result['temperature']}°C")
                return result

        except httpx.RequestError as e:
            logger.error(f"[ERROR] API Request failed (connection/timeout): {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"[ERROR] API returned error status: {e.response.status_code}. Check API key or city name.")
            return None
        except Exception as e:
            logger.error(f"[ERROR] An unexpected error occurred during API fetch: {e}")
            return None
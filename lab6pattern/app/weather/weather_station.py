import logging
import asyncio
from typing import List, Dict, Callable, Coroutine, Any, Optional

from ..core.config import settings
from ..db.models import WeatherData
from .weather_api import OpenWeatherMapAPI

logger = logging.getLogger("planner_app")

# Визначення типу для асинхронного методу оновлення спостерігача
ObserverUpdateMethod = Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]


class WeatherStation:
    """
    WeatherStation є СУБ'ЄКТОМ (Subject/Observable) в Observer Pattern.
    Він перевіряє погоду та сповіщає DayPlanner про зміни.
    """

    def __init__(self, api_key: str, city: str):
        self._api = OpenWeatherMapAPI(api_key, city)
        self._observers: List[ObserverUpdateMethod] = []
        self.current_weather: Optional[WeatherData] = None

    def attach(self, observer_update_method: ObserverUpdateMethod):
        """Додає DayPlanner.update до списку спостерігачів."""
        if observer_update_method not in self._observers:
            self._observers.append(observer_update_method)
            logger.info("DayPlanner attached to WeatherStation.")

    def detach(self, observer_update_method: ObserverUpdateMethod):
        """Видаляє спостерігача."""
        self._observers.remove(observer_update_method)

    async def notify(self, new_weather_data: dict):
        """Сповіщає всіх спостерігачів (DayPlanner) про оновлення."""
        logger.info(f"Notifying {len(self._observers)} observers...")
        tasks = [observer(new_weather_data) for observer in self._observers]
        # Запускаємо всі оновлення паралельно
        await asyncio.gather(*tasks)

    async def check_for_update(self):
        """
        Перевіряє погоду. Якщо вона змінилася, сповіщає спостерігачів.
        """
        logger.info("[TASK] Checking weather update...")
        new_data: Optional[dict] = await self._api.fetch_weather_data()

        if not new_data:
            logger.error("Could not get new weather data. Skipping update.")
            return

        new_weather = WeatherData(**new_data)

        # Перевірка, чи змінилася основна умова (Sunny, Rainy, Cloudy, Snowy)
        condition_changed = (self.current_weather is None or
                             self.current_weather.condition != new_weather.condition)

        if condition_changed:
            logger.info(
                f"[WEATHER] Condition change detected: {self.current_weather.condition if self.current_weather else 'N/A'} -> {new_weather.condition}")
            self.current_weather = new_weather

            # Сповіщення спостерігачів
            await self.notify(new_weather.model_dump())
        else:
            self.current_weather = new_weather
            logger.info(f"[WEATHER] Condition is the same ({new_weather.condition}). Temperature updated.")
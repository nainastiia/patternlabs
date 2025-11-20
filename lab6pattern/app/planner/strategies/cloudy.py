from .base import WeatherStrategy, ALL_ACTIVITIES
from ...db.models import Activity, UserPreferences
from typing import List


class CloudyWeatherStrategy(WeatherStrategy):
    """
    Конкретна Стратегія для Хмарної Погоди.
    Пріоритет: Гнучкі активності та помірні зовнішні.
    """

    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        # Активності, які добре підходять для хмарності
        cloudy_candidates = [
            a for a in ALL_ACTIVITIES
            if a.get_activity().type in ["productive", "indoor"]
        ]

        # Додаємо спорт як помірну зовнішню/внутрішню активність
        sport_candidate = [a for a in ALL_ACTIVITIES if a.get_activity().type == "sport"]

        combined_activities = cloudy_candidates + sport_candidate
        return self._filter_and_prioritize(combined_activities, preferences)
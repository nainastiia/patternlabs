from .base import WeatherStrategy, ALL_ACTIVITIES
from ...db.models import Activity, UserPreferences
from typing import List


class SnowyWeatherStrategy(WeatherStrategy):
    """
    Конкретна Стратегія для Сніжної Погоди.
    Пріоритет: Спеціальні зимові активності або затишні заняття в приміщенні.
    """

    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        # Затишні заняття в приміщенні (HouseWork, Studying)
        indoor_candidates = [
            a for a in ALL_ACTIVITIES
            if a.get_activity().type in ["indoor", "productive"]
        ]

        combined_activities = indoor_candidates
        return self._filter_and_prioritize(combined_activities, preferences)
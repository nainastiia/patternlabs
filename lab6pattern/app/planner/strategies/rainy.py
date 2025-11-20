from .base import WeatherStrategy, ALL_ACTIVITIES
from ...db.models import Activity, UserPreferences
from typing import List


class RainyWeatherStrategy(WeatherStrategy):
    """
    Конкретна Стратегія для Дощової Погоди.
    Пріоритет: Активності в приміщенні та продуктивні справи.
    """

    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        # Активності, які добре підходять для дощу
        rainy_candidates = [
            a for a in ALL_ACTIVITIES
            if a.get_activity().type in ["indoor", "productive"]
        ]

        # Додаємо спорт (припускаємо, що це спорт у приміщенні) та побачення
        backup_candidates = [
            a for a in ALL_ACTIVITIES
            if a.get_activity().type in ["sport"]
        ]

        combined_activities = rainy_candidates + backup_candidates
        return self._filter_and_prioritize(combined_activities, preferences)
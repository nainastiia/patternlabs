from .base import WeatherStrategy, ALL_ACTIVITIES
from ...db.models import Activity, UserPreferences
from typing import List


class SunnyWeatherStrategy(WeatherStrategy):
    """
    Конкретна Стратегія для Сонячної Погоди.
    Пріоритет: Активності на свіжому повітрі.
    """

    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        # Фільтрація інстансів активностей, які підходять для сонячної погоди
        sunny_candidates = [
            a for a in ALL_ACTIVITIES
            if a.get_activity().type in ["outdoor", "sport", "indoor"]
        ]

        # Додаємо продуктивні та домашні справи як запасний варіант
        backup_candidates = [
            a for a in ALL_ACTIVITIES
            if a.get_activity().type in ["productive", "indoor"]
        ]

        combined_activities = sunny_candidates + backup_candidates
        return self._filter_and_prioritize(combined_activities, preferences)
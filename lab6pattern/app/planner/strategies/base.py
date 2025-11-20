from abc import ABC, abstractmethod
from typing import List
from ...db.models import Activity, UserPreferences

# Імпортуємо всі конкретні класи активностей для їхнього використання стратегіями
from ..activities.base import BaseActivity
from ..activities.hiking import Hiking
from ..activities.housework import Housework
from ..activities.sport import Sport
from ..activities.studying import Studying

# Створення єдиного списку ВСІХ можливих активностей
ALL_ACTIVITIES: List[BaseActivity] = [
    Hiking(),
    Housework(),
    Studying(),
    Sport(),
    # Додайте інші класи активностей тут, наприклад MovieNight, Skiing
]


class WeatherStrategy(ABC):#клас для всіх стратегій

    @abstractmethod
    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        """Генерує список активностей на основі погоди та уподобань користувача."""
        pass

    def _filter_and_prioritize(self, activity_candidates: List[BaseActivity], preferences: UserPreferences) -> List[
        Activity]:
        """Загальна логіка фільтрації, пріоритизації та перетворення в Pydantic модель"""

        processed_activities = []#зберігання відфільтрованих та оновлених активностей
        avoid_types = set(preferences.avoid_types)
        preferred_types = set(preferences.preferred_types)#множину бажаних типів

        for activity_instance in activity_candidates:
            activity = activity_instance.get_activity()  # Отримуємо Pydantic модель

            # 1. Фільтрація
            if activity.type in avoid_types:
                continue

            # 2. Пріоритизація
            score = activity.priority
            if activity.type in preferred_types:
                score += 2  # Бонус за бажаний тип

            # 3. Обробка вихідних
            if preferences.weekend_mode and activity.type == "productive":
                score -= 3  # Знижуємо пріоритет для продуктивних на вихідних

            # Створення копії активності з оновленим пріоритетом
            updated_activity = activity.copy(update={'priority': score})
            processed_activities.append(updated_activity)

        # Сортування: вищий пріоритет на початку, обмеження до 6
        return sorted(processed_activities, key=lambda a: a.priority, reverse=True)[:6]
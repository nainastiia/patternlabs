import logging
from typing import Optional

from ..db.models import ActivityPlan, UserPreferencesDB, UserPreferences
from ..core.config import settings
from ..db.mongodb import db
from ..planner.strategies.base import WeatherStrategy
from .strategies.sunny import SunnyWeatherStrategy
from .strategies.rainy import RainyWeatherStrategy
from .strategies.cloudy import CloudyWeatherStrategy
from .strategies.snowy import SnowyWeatherStrategy

logger = logging.getLogger("planner_app")


class DayPlanner:
    """
    DayPlanner є КОНТЕКСТОМ (Strategy Pattern) та СПОСТЕРІГАЧЕМ (Observer Pattern).
    """

    def __init__(self, db_client):
        self.db_client = db_client  # Клієнт MongoDB
        self._current_weather_condition: Optional[str] = None

    def _get_strategy(self, condition: str) -> WeatherStrategy:
        """Вибирає конкретну стратегію на основі умови погоди."""
        condition = condition.lower()
        if "sunny" in condition or "clear" in condition:
            return SunnyWeatherStrategy()
        elif "rainy" in condition or "drizzle" in condition:
            return RainyWeatherStrategy()
        elif "cloudy" in condition or "clouds" in condition or "mist" in condition:
            return CloudyWeatherStrategy()
        elif "snowy" in condition or "snow" in condition:
            return SnowyWeatherStrategy()
        else:
            logger.warning(f"Unknown weather condition: {condition}. Falling back to Cloudy.")
            return CloudyWeatherStrategy()

    async def _get_user_preferences(self, user_id: str) -> UserPreferences:
        """Отримує уподобання користувача з MongoDB, або створює за замовчуванням."""

        pref_collection = self.db_client[db.DATABASE_NAME]["preferences"]
        preferences_doc = await pref_collection.find_one({"user_id": user_id})

        if preferences_doc:
            preferences_doc.pop('_id', None)
            return UserPreferencesDB(**preferences_doc).preferences

        logger.warning(f"Preferences not found for user_id: {user_id}. Creating defaults.")
        # Створення запису за замовчуванням
        default_prefs = UserPreferences()
        await pref_collection.insert_one(
            UserPreferencesDB(user_id=user_id, preferences=default_prefs).model_dump(by_alias=True))
        return default_prefs

    async def generate_plan(self, weather_data: dict, user_id: str = "default_user") -> ActivityPlan:
        """
        Генерує план: 
        1. Отримує уподобання. 2. Вибирає та виконує стратегію. 3. Зберігає.
        """
        condition = weather_data.get("condition", "Cloudy")

        strategy = self._get_strategy(condition)
        preferences = await self._get_user_preferences(user_id)

        # Виконання стратегії
        activities = strategy.get_activities(preferences)

        plan = ActivityPlan(
            location=weather_data.get("location", settings.WEATHER_CITY),
            weather=weather_data,
            activities=activities,
            user_id=user_id
        )

        await self._save_plan(plan)
        return plan

    async def _save_plan(self, plan: ActivityPlan):
        """Зберігає новий план у MongoDB."""
        plan_dict = plan.model_dump(by_alias=True)
        plan_collection = self.db_client[db.DATABASE_NAME]["plans"]

        await plan_collection.update_one(
            {"user_id": plan.user_id, "date": plan.date},
            {"$set": plan_dict},
            upsert=True
        )

    # --- Observer Pattern Method ---
    async def update(self, new_weather_data: dict):
        """Метод, який викликається Subject (WeatherStation) при зміні погоди."""
        new_condition = new_weather_data.get("condition")
        old_condition = self._current_weather_condition
        self._current_weather_condition = new_condition

        logger.info(
            f"[INFO] DayPlanner notified. Weather change: {old_condition if old_condition else 'N/A'} -> {new_condition}")

        try:
            # Перегенеруємо план для користувача за замовчуванням
            plan = await self.generate_plan(new_weather_data, user_id="default_user")

            first_new_activity = plan.activities[0].name if plan.activities else "No activity"

            logger.info(f"[INFO] Plan successfully updated. New top activity: {first_new_activity}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to regenerate plan after weather update: {e}")
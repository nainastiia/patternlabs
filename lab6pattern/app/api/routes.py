from fastapi import APIRouter, HTTPException, Request, Depends
from ..db.models import ActivityPlan, UserPreferencesDB, UserPreferences
from ..db.mongodb import db
from ..weather.weather_station import WeatherStation
import logging

logger = logging.getLogger("planner_app")


# Залежність для отримання об'єкта WeatherStation
def get_weather_station(request: Request) -> WeatherStation:
    return request.app.state.weather_station


router = APIRouter(prefix="/api")


# --- Плани та Погода ---

@router.get("/plan/current/{user_id}", response_model=ActivityPlan)
async def get_current_plan(user_id: str):
    """Отримує останній згенерований план для користувача."""
    plan_collection = db.client[db.DATABASE_NAME]["plans"]#доступ до колекції "plans"
    plan_doc = await plan_collection.find_one(#шукає один документ
        {"user_id": user_id},
        sort=[("created_at", -1)]  # Останній за часом
    )
    if not plan_doc:
        raise HTTPException(status_code=404, detail="Plan not found. Please click 'Refresh Plan Now' to generate one.")

    plan_doc.pop('_id', None)
    return ActivityPlan(**plan_doc)


@router.post("/weather/force_update")
async def force_weather_update(ws: WeatherStation = Depends(get_weather_station)):
    """Примусово запускає перевірку погоди та оновлення плану."""
    logger.info("API request to force weather update.")
    # WeatherStation перевірить погоду і, якщо вона змінилася, сповістить DayPlanner
    await ws.check_for_update()#метод перевірки погоди
    return {"status": "success", "message": "Weather check initiated. Check logs for plan update status."}


# --- Уподобання Користувача ---

@router.get("/preferences/{user_id}", response_model=UserPreferences)
async def get_preferences(user_id: str):
    """Отримує уподобання користувача."""
    pref_collection = db.client[db.DATABASE_NAME]["preferences"]
    pref_doc = await pref_collection.find_one({"user_id": user_id})
    if not pref_doc:
        raise HTTPException(status_code=404, detail="User preferences not found.")

    return UserPreferencesDB(**pref_doc).preferences.model_dump()


@router.put("/preferences/{user_id}", response_model=UserPreferences)
async def update_preferences(user_id: str, preferences: UserPreferences):
    """Оновлює або створює уподобання користувача."""
    pref_db = UserPreferencesDB(user_id=user_id, preferences=preferences)
    pref_collection = db.client[db.DATABASE_NAME]["preferences"]

    result = await pref_collection.update_one(
        {"user_id": user_id},
        {"$set": pref_db.model_dump(by_alias=True)},
        upsert=True
    )
    logger.info(f"[DB] Preferences updated for {user_id}. Upserted: {result.upserted_id}")
    return preferences
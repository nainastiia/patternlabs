import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .core.config import settings
from .core.logger import setup_logging
from .db.mongodb import connect_to_mongo, close_mongo_connection, db
from .weather.weather_station import WeatherStation
from .planner.day_planner import DayPlanner
from .tasks.scheduler import start_scheduler, shutdown_scheduler
from .api.routes import router as api_router

# Налаштування логування
setup_logging()
logger = logging.getLogger("planner_app")

# Ініціалізація FastAPI
app = FastAPI(
    title="Smart Day Planner (lab6pattern)",
    version="1.0.0",
    description="Uses Strategy and Observer patterns to adapt plans based on weather."
)


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup initiated.")
    try:
        await connect_to_mongo()

        # 1. Ініціалізація компонентів
        app.state.weather_station = WeatherStation(
            api_key=settings.OPENWEATHER_API_KEY,
            city=settings.WEATHER_CITY
        )
        app.state.planner = DayPlanner(
            db_client=db.client
        )

        # 2. Observer Pattern: Приєднуємо DayPlanner до WeatherStation
        app.state.weather_station.attach(app.state.planner.update)

        # 3. Виконання першої перевірки негайно
        logger.info("Executing initial weather check and plan generation.")
        await app.state.weather_station.check_for_update()

        # 4. Запуск періодичного завдання
        start_scheduler(app.state.weather_station)

        logger.info("Application startup complete.")
    except Exception as e:
        logger.error(f"FATAL: Error during startup: {e}")
        # Тут можна ініціювати graceful shutdown, але для простоти ми продовжуємо


@app.on_event("shutdown")
async def shutdown_event():
    shutdown_scheduler()
    await close_mongo_connection()
    logger.info("Application shutdown complete.")


# --- Додавання API маршрутів та Frontend ---
app.include_router(api_router)

# Обслуговування статичних файлів (CSS)
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

# Налаштування шаблонів Jinja2
templates = Jinja2Templates(directory="app/frontend/templates")


# Головний маршрут для фронтенду
@app.get("/", include_in_schema=False)
async def serve_frontend(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_title": app.title}
    )
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
#планувальник завдань, оптимізований для роботи з asyncio
from ..core.config import settings
from ..weather.weather_station import WeatherStation

logger = logging.getLogger("planner_app")

scheduler = AsyncIOScheduler()#глобальний екземпляр планувальника


def start_scheduler(weather_station: WeatherStation):
    """Ініціалізує та запускає APScheduler."""

    # Визначаємо завдання
    scheduler.add_job( #додавання нового завдання до планувальника
        weather_station.check_for_update,
        trigger=IntervalTrigger(seconds=settings.WEATHER_CHECK_INTERVAL),
        id='weather_check_job',
        name='Periodic Weather Check',
        replace_existing=True,
        max_instances=1
    )

    if not scheduler.running:
        #чи планувальник ще не запущений
        scheduler.start()
        logger.info(f"Scheduler started. Weather check every {settings.WEATHER_CHECK_INTERVAL} seconds.")


def shutdown_scheduler():#вимкнення планувальника
    """Зупиняє планувальник при вимкненні FastAPI."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down.")
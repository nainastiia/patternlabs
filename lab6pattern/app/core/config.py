import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://mongo:27017/plannerDB")
    DATABASE_NAME: str = "plannerDB"

    # OpenWeatherMap API
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    WEATHER_CITY: str = os.getenv("WEATHER_CITY", "Kyiv")

    # Scheduling (in seconds)
    WEATHER_CHECK_INTERVAL: int = 1800  # 30 minutes
    #інтервал перевірки погоди


settings = Settings() #єдиний екземпляр класу
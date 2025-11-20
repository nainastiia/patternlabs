from motor.motor_asyncio import AsyncIOMotorClient#асинхронний клієнт MongoDB
from ..core.config import settings
import logging

logger = logging.getLogger("planner_app")

class MongoDB: #клас-контейнер для клієнта
    client: AsyncIOMotorClient = None
    DATABASE_NAME: str = settings.DATABASE_NAME

db = MongoDB()#глобальний екземпляр `MongoDB` (singleton)

async def connect_to_mongo():
    """Встановлює з'єднання з MongoDB."""
    logger.info("Connecting to MongoDB...")
    # Використовуємо ім'я сервісу 'mongo' з docker-compose
    db.client = AsyncIOMotorClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=5000#тайм-аут для вибору сервера
    )
    try:
        # Перевірка з'єднання
        await db.client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB: {db.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        # Завершити роботу, якщо з'єднання не встановлено
        raise RuntimeError("Failed to connect to MongoDB.")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed.")
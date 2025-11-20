import logging

#налаштування логування
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    # Зниження рівня логування для деяких бібліотек
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
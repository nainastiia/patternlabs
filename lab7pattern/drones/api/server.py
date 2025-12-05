from fastapi import FastAPI
from drones.api.endpoints import router  # обов’язково абсолютний імпорт

app = FastAPI(
    title="Drone API",
    description="API для керування місіями дронів",
    version="1.0.0"
)

# Підключаємо роутер
app.include_router(router, prefix="/api")

# Тестовий корінь
@app.get("/")
def root():
    return {"message": "Drone API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

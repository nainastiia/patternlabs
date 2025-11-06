from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from devices.base_device import Device


# --- Клас стану лампи ---
class LightState(BaseModel):
    is_on: bool = False
    brightness: int = 50


# --- Основний клас пристрою ---
class SmartLightDevice(Device):
    def __init__(self, device_id: str, host="127.0.0.1", port=8002):
        super().__init__(device_id, host, port)
        self.state = LightState()
        self.app = FastAPI(title=f"Smart Light {device_id}")
        self._setup_routes()

    def _setup_routes(self):
        app = self.app

        # --- HTML-інтерфейс ---
        @app.get("/", response_class=HTMLResponse)
        def index():
            return """
            <html>
                <head>
                    <title>Smart Light</title>
                    <script>
                        async function sendPost(url) {
                            const response = await fetch(url, {method: 'POST'});
                            if (response.ok) {
                                alert('Дія виконана успішно!');
                            } else {
                                const data = await response.json();
                                alert('Помилка: ' + (data.detail || 'невідома'));
                            }
                        }
                        
                        async function checkStatus() {
                            const response = await fetch('/status'); 
                            if (response.ok) {
                                const data = await response.json();
                                alert(
                                    'Статус світла:\\n' +
                                    'Увімкнено: ' + (data.is_on ? 'Так' : 'Ні') + '\\n' +
                                    'Яскравість: ' + data.brightness + '%'
                                );
                            } else {
                                const data = await response.json();
                                alert('Помилка: ' + (data.detail || 'невідома'));
                            }
                        }
                    </script>
                </head>
                <body style="font-family: sans-serif;">
                    <h1>Smart Light</h1>
                    <p>Поточний стан: <a href="#" onclick="checkStatus()">перевірити</a></p>
                    <p>
                        <a href="#" onclick="sendPost('/power/on')">Увімкнути</a> |
                        <a href="#" onclick="sendPost('/power/off')">Вимкнути</a>
                    </p>
                    <p>
                        Змінити яскравість:
                        <a href="#" onclick="sendPost('/brightness/25')">25%</a> |
                        <a href="#" onclick="sendPost('/brightness/50')">50%</a> |
                        <a href="#" onclick="sendPost('/brightness/75')">75%</a> |
                        <a href="#" onclick="sendPost('/brightness/100')">100%</a>
                    </p>
                </body>
            </html>
            """

        # --- REST API ---
        @app.get("/status")
        async def get_status():
            return self.get_status()

        @app.post("/power/{state}")
        async def set_power(state: str):
            state = state.lower()
            if state == "on":
                self.state.is_on = True
            elif state == "off":
                self.state.is_on = False

        @app.post("/brightness/{level}")
        async def set_brightness(level: int):
            if 0 <= level <= 100:
                self.state.brightness = level

    # --- Отримати статус ---
    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": "smart_light",
            "is_on": self.state.is_on,
            "brightness": self.state.brightness,
            "connection": f"{self.host}:{self.port}"
        }

    # --- Запуск сервера ---
    def run_server(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def perform_action(self, action: str, **kwargs) -> bool:
        # Успішно обробляємо локальний виклик, щоб Decorator не видав помилку
        return True


# --- Точка входу ---
if __name__ == "__main__":
    light = SmartLightDevice("light_001")
    light.run_server()

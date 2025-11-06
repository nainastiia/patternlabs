from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from devices.base_device import Device


class CurtainState(BaseModel):
    is_open: bool = False
    position: int = 0


class SmartCurtainsDevice(Device):
    def __init__(self, device_id: str, host="127.0.0.1", port=8003):
        super().__init__(device_id, host, port)
        self.state = CurtainState()
        self.app = FastAPI(title=f"Smart Curtains {device_id}")
        self._setup_routes()

    def _setup_routes(self):
        app = self.app

        # --- HTML головна сторінка ---
        @app.get("/", response_class=HTMLResponse)
        def index():
            return """
            <html>
                <head>
                    <title>Smart Curtains</title>
                    <script>
                        async function sendPost(url) {
                            const response = await fetch(url, { method: 'POST' });
                            if (response.ok) {
                                alert('Дія виконана успішно!');
                            } else {
                                const data = await response.json();
                                alert('Помилка: ' + (data.detail || 'невідома'));
                            }
                        }
                        
                        async function checkStatus() {
                            const response = await fetch('/status'); // GET запит
                            if (response.ok) {
                                const data = await response.json();
                                alert(
                                    'Статус штор:\\n' +
                                    'Відкрито: ' + (data.is_open ? 'Так' : 'Ні') + '\\n' +
                                    'Позиція: ' + data.position + '%'
                                );
                            } else {
                                const data = await response.json();
                                alert('Помилка: ' + (data.detail || 'невідома'));
                            }
                        }
                    </script>
                </head>
                <body style="font-family: sans-serif;">
                    <h1>Smart Curtains</h1>
                    <p>Поточний стан: <a href="#" onclick="checkStatus()">перевірити</a></p>
                    <p>
                        <a href="#" onclick="sendPost('/power/open')">Відкрити</a> |
                        <a href="#" onclick="sendPost('/power/close')">Закрити</a>
                    </p>
                    <p>
                        Змінити позицію:
                        <a href="#" onclick="sendPost('/position/25')">25%</a> |
                        <a href="#" onclick="sendPost('/position/50')">50%</a> |
                        <a href="#" onclick="sendPost('/position/75')">75%</a> |
                        <a href="#" onclick="sendPost('/position/100')">100%</a>
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
            if state == "open":
                self.state.is_open = True
                self.state.position = 100
            elif state == "close":
                self.state.is_open = False
                self.state.position = 0

        @app.post("/position/{value}")
        async def set_position(value: int):
            if 0 <= value <= 100:
                self.state.position = value
                self.state.is_open = value > 0

    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": "smart_curtains",
            "is_open": self.state.is_open,
            "position": self.state.position,
            "connection": f"{self.host}:{self.port}"
        }

    def run_server(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def perform_action(self, action: str, **kwargs) -> bool:
        # Успішно обробляємо локальний виклик, щоб Decorator не видав помилку
        return True


if __name__ == "__main__":
    curtains = SmartCurtainsDevice("curtains_001")
    curtains.run_server()

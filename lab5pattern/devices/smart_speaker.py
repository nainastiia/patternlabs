from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from devices.base_device import Device


# --- Клас стану ---
class SpeakerState(BaseModel):
    is_on: bool = False
    volume: int = 25
    playing: bool = False
    current_track: str = ""


# --- Основний клас пристрою ---
class SmartSpeakerDevice(Device):
    #Створює FastAPI сервер
    def __init__(self, device_id: str, host="127.0.0.1", port=8001):
        super().__init__(device_id, host, port)
        self.state = SpeakerState()
        self.app = FastAPI(title=f"Smart Speaker {device_id}")
        self._setup_routes()

    def _setup_routes(self):
        app = self.app

        # --- HTML-інтерфейс ---
        @app.get("/", response_class=HTMLResponse)
        def index():
            return """
            <html>
                <head>
                    <title>Smart Speaker</title>
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
                            const response = await fetch('/status');  // GET запит
                            if (response.ok) {
                                const data = await response.json();
                                alert(
                                    'Статус динаміка:\\n' +
                                    'Увімкнено: ' + (data.is_on ? 'Так' : 'Ні') + '\\n' +
                                    'Гучність: ' + data.volume + '%\\n' +
                                    'Відтворюється: ' + (data.playing ? 'Так' : 'Ні') + '\\n' +
                                    'Поточний трек: ' + data.current_track
                                );
                            } else {
                                const data = await response.json();
                                alert('Помилка: ' + (data.detail || 'невідома'));
                            }
                        }
                    </script>
                </head>
                <body style="font-family: sans-serif;">
                    <h1>Smart Speaker</h1>

                    <p>Поточний стан: <a href="#" onclick="checkStatus()">перевірити</a></p>

                    <p>
                        <a href="#" onclick="sendPost('/power/on')">Увімкнути</a> |
                        <a href="#" onclick="sendPost('/power/off')">Вимкнути</a>
                    </p>

                    <p>Гучність: 
                        <a href="#" onclick="sendPost('/volume/25')">25%</a> |
                        <a href="#" onclick="sendPost('/volume/50')">50%</a> |
                        <a href="#" onclick="sendPost('/volume/75')">75%</a> |
                        <a href="#" onclick="sendPost('/volume/100')">100%</a>
                    </p>

                    <p>Відтворення: 
                        <a href="#" onclick="sendPost('/play')">Відтворити</a> |
                        <a href="#" onclick="sendPost('/pause')">Пауза</a>
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
                self.state.playing = False  #При вимкненні автоматично ставиться пауза

        @app.post("/volume/{level}")
        async def set_volume(level: int):
            if 0 <= level <= 100:
                self.state.volume = level

        @app.post("/play")
        async def play_music():
            if not self.state.is_on:
                raise HTTPException(status_code=400, detail="Speaker is off")
            self.state.playing = True
            self.state.current_track = "Track 1"

        @app.post("/pause")
        async def pause_music():
            if not self.state.is_on or not self.state.playing:
                raise HTTPException(status_code=400, detail="Speaker is off or not playing")
            self.state.playing = False

    # --- Логіка пристрою ---
    def get_status(self) -> Dict[str, Any]:
        #виклик в html, записує в json, js переводить в alert
        return {
            "device_id": self.device_id,
            "type": "smart_speaker",
            "is_on": self.state.is_on,
            "volume": self.state.volume,
            "playing": self.state.playing,
            "current_track": self.state.current_track,
            "connection": f"{self.host}:{self.port}"
        }

    # --- Запуск ---
    def run_server(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def perform_action(self, action: str, **kwargs) -> bool:
        # Успішно обробляємо локальний виклик, щоб Decorator не видав помилку
        return True


# --- Точка входу ---
if __name__ == "__main__":
    speaker = SmartSpeakerDevice("speaker_001")
    speaker.run_server()

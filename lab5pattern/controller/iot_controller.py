from typing import Dict, Any, List, Optional
import requests
from requests.exceptions import RequestException

class IotController:
    """
    Facade that abstracts HTTP communication with device microservices.
    Devices are registered as objects that have device_id, host, port attributes.
    """

    def __init__(self, timeout: float = 1.0):
        self._devices: Dict[str, object] = {}
        self.timeout = timeout#для запитів до пристроїв

    def register_device(self, device: object) -> str:
        #Перевіряє, що пристрій має device_id
        device_id = getattr(device, "device_id", None)
        if not device_id:
            raise ValueError("Device must have device_id")
        self._devices[device_id] = device
        return device_id

    def get_registered_ids(self) -> List[str]:
        return list(self._devices.keys())

    def _base_url(self, device_id: str) -> str:
        #Формує базовий URL для HTTP-запитів до конкретного пристрою
        device = self._devices.get(device_id)
        if not device:
            raise KeyError(f"Device {device_id} not registered")
        host = getattr(device, "host")
        port = getattr(device, "port")
        return f"http://{host}:{port}"

    def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Call GET /status on device microservice"""
        try:
            url = self._base_url(device_id) + "/status"
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except (KeyError, RequestException):
            return None

    def perform_device_action(self, device_id: str, action: str, **kwargs) -> bool:
        """
        Map logical actions to device endpoints.
        Expected endpoints:
         - POST /power/{state}
         - POST /position/{value}
         - POST /set_volume/{level} or POST /volume/{level}
         - POST /set_brightness/{level} or POST /brightness/{level}
        We will attempt several reasonable endpoints for compatibility.
        """
        try:
            base = self._base_url(device_id)
            #Визначає URL для POST-запиту
        except KeyError:
            return False

        #Формує URL відповідно до типу дії
        # Це робить усі POST-запити централізовано через Facade

        # power action
        if action == "power":
            state = kwargs.get("state")
            if state is None: return False
            url = f"{base}/power/{state}"

        # Action: volume
        elif action == "volume":
            level = kwargs.get("level")
            if level is None: return False
            url = f"{base}/volume/{int(level)}"

        # Action: brightness
        elif action == "brightness":
            level = kwargs.get("level")
            if level is None: return False
            url = f"{base}/brightness/{int(level)}"

        # Action: position
        elif action == "position":
            value = kwargs.get("value")
            if value is None: return False
            url = f"{base}/position/{int(value)}"

        # Action: play/pause
        elif action in ("play", "pause"):
            url = f"{base}/{action}"

        else:
            return False

        #Виконує POST-запит

        try:
            resp = requests.post(url, timeout=self.timeout)
            if 200 <= resp.status_code < 300:
                return True
        except RequestException:
            pass

        return False

    def get_all_status(self) -> List[Dict[str, Any]]:
        statuses = []
        for device_id in self._devices:
            status = self.get_device_status(device_id)
            if status is None:
                statuses.append({
                    "device_id": device_id,
                    "type": "unknown",
                    "error": "unreachable",
                    "connection": f"{getattr(self._devices[device_id], 'host')}:{getattr(self._devices[device_id], 'port')}"
                })
            else:
                statuses.append(status)
        return statuses

from typing import Dict, Any

class Device:
    """Base IoT Device (used as a registration descriptor for facade)"""
    def __init__(self, device_id: str, host: str, port: int):
        self.device_id = device_id
        self.host = host
        self.port = port

    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError()

    def perform_action(self, action: str, **kwargs) -> bool:
        raise NotImplementedError()

    def run_server(self):
        raise NotImplementedError()


class LoggingDeviceDecorator(Device):
    """Decorator that wraps a Device instance to add logging for local operations.
       When registered in facade, facade will only use host/port; logging decorator adds
       helpful prints on the controller side.
    """
    def __init__(self, device: Device):
        super().__init__(device.device_id, device.host, device.port)
        self._device = device

    def get_status(self):
        print(f"[LOG] Request status for {self.device_id} at {self.host}:{self.port}")
        try:
            return self._device.get_status()
        except Exception:
            return {}

    def perform_action(self, action: str, **kwargs):
        print(f"[LOG] Perform {action} on {self.device_id} with {kwargs}")
        try:
            return self._device.perform_action(action, **kwargs)
        except Exception:
            # As above — fallback: facade will attempt HTTP
            return False

    def run_server(self):
        print(f"[LOG] Running server for {self.device_id}")
        return self._device.run_server()

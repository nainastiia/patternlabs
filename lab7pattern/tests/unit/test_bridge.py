from drones.bridge.air import AirPlatform
from drones.bridge.controller import DroneController

def test_bridge():
    ctrl = DroneController(AirPlatform())
    assert ctrl.goto((1,2,3)) is None

from drones.missions.rescue import Rescue

def test_template():
    assert hasattr(Rescue, "execute_mission")

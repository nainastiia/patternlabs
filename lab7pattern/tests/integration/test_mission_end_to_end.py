from drones.factory.mission_factory import MissionFactory

def test_integration():
    factory = MissionFactory()
    cfg = {
        "mission_id": "1",
        "mission_type": "rescue",
        "environment_type": "air",
        "platform_type": "air",
        "mode": "single",
        "target_area": (1,2,3),
        "base_area": (0,0,0),
        "thresholds": {},
        "behavior_params": {}
    }

    m = factory.create_from_dict(cfg)
    result = m.execute_mission()
    assert result["status"] == "DONE"

import json
from ..config.mission_config import MissionConfig


class ConfigLoader:

    @staticmethod
    def from_dict(data: dict) -> MissionConfig:
        return MissionConfig(
            mission_id=data["mission_id"],
            mission_type=data["mission_type"],
            environment_type=data["environment_type"],
            platform_type=data["platform_type"],
            mode=data["mode"],
            target_area=tuple(data["target_area"]),
            base_area=tuple(data["base_area"]),
            thresholds=data.get("thresholds", {}),
            behavior_params=data.get("behavior_params", {})
        )

    @staticmethod
    def from_json(file_path: str) -> MissionConfig:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ConfigLoader.from_dict(data)

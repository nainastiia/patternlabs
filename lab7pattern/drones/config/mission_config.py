from dataclasses import dataclass
from typing import Tuple, Dict, Any


Coord = Tuple[float, float, float]  # (x, y, z)


@dataclass
class MissionConfig:
    mission_id: str
    mission_type: str
    environment_type: str
    platform_type: str
    mode: str
    target_area: Coord
    base_area: Coord
    thresholds: Dict[str, float]
    behavior_params: Dict[str, Any]

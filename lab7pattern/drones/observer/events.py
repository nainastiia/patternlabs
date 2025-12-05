from dataclasses import dataclass

@dataclass
class EnvironmentEvent:
    type: str
    data: dict
    severity: int = 1

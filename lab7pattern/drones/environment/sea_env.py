import random
from .base import Environment

class SeaEnvironment(Environment):
    def sample(self):
        wave = random.uniform(0, 3)# Генерує випадкову висоту хвилі
        return {"type": "wave", "data": {"height": wave}}

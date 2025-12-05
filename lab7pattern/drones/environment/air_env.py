import random
from .base import Environment

class AirEnvironment(Environment):
    def sample(self):
        wind = random.uniform(0, 20)# Генерує випадкову швидкість вітру
        return {"type": "wind", "data": {"speed": wind}}

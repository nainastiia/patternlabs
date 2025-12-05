import random
from .base import Environment

class SurfaceEnvironment(Environment):
    def sample(self):
        cracks = random.randint(0, 5)# Генерує випадкову кількість тріщин/дефектів
        return {"type": "crack", "data": {"count": cracks}}

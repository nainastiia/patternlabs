from typing import Callable, List

class EventBus:#реалізує центральний механізм Спостерігача
    def __init__(self):
        self.subscribers: List[Callable] = []

    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)

    def publish(self, event: dict):
        for subscriber in self.subscribers:
            subscriber(event)

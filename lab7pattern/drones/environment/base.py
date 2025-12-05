from abc import ABC, abstractmethod
from ..observer.event_bus import EventBus

class Environment(ABC):

    def __init__(self, bus: EventBus):
        self.bus = bus

    @abstractmethod
    def sample(self) -> dict: ...

    def start(self):#для запуску збору даних
        event = self.sample()
        self.bus.publish(event)

    def subscribe(self, callback):#для підписки на події середовища
        self.bus.subscribe(callback)

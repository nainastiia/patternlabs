from abc import ABC, abstractmethod
from typing import Tuple

Coord = Tuple[float, float, float]

class MovementImplementor(ABC):

    @abstractmethod
    def takeoff(self): ... #для старту

    @abstractmethod
    def land(self): ... #для завершення

    @abstractmethod
    def move_to(self, coord: Coord): ...#для переміщення

    @abstractmethod
    def adjust_course(self, vector: Coord): ...#для коригування курсу

    @abstractmethod
    def hold_position(self): ...#для утримання позиції

    @abstractmethod
    def set_mode(self, mode: str): ...#для встановлення режиму роботи

    @abstractmethod
    def broadcast(self, message: str): ...#для широкомовного повідомлення

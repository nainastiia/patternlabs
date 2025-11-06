from abc import ABC, abstractmethod

class Container(ABC):
    def __init__(self, id_: int, weight: int):
        self.id_ = id_
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        pass

    def __eq__(self, other):
        return isinstance(other, Container) and self.id_ == other.id_ and self.weight == other.weight

class BasicContainer(Container):
    def consumption(self) -> float:
        return 0.025 * self.weight

class HeavyContainer(Container):
    def consumption(self) -> float:
        return 0.03 * self.weight

class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return 0.05 * self.weight

class LiquidContainer(HeavyContainer):
    def consumption(self) -> float:
        return 0.04 * self.weight

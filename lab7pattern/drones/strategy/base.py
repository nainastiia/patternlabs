from abc import ABC, abstractmethod

class ReactionStrategy(ABC):

    @abstractmethod
    def react(self, mission, reading): ...

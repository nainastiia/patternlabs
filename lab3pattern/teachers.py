from abc import ABC, abstractmethod

class Teacher(ABC):
    """Abstract base class for teachers."""

    def __init__(self, name: str):
        """Initialize with teacher's name."""
        self.name = name

    def __repr__(self):
        """Return class name and teacher's name."""
        return f"{self.__class__.__name__}({self.name})"

    @abstractmethod
    def do(self):
        """Perform teacher's main activity."""
        pass


class Lecturer(Teacher):
    """Lecturer giving lectures."""

    def do(self) -> str:
        """Return lecturer's action."""
        return f"{self.name} is giving a lecture."


class Assistant(Teacher):
    """Assistant leading practicals."""

    def do(self) -> str:
        """Return assistant's action."""
        return f"{self.name} is leading a practical class."


class ExternalMentor(Teacher):
    """External mentor supervising works."""

    def do(self) -> str:
        """Return mentor's action."""
        return f"{self.name} is supervising course works."

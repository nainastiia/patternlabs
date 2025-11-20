from abc import ABC, abstractmethod
from ...db.models import Activity


class BaseActivity(ABC):
    """Базовий клас для всіх конкретних активностей."""

    @abstractmethod
    def get_activity(self) -> Activity:
        """Повертає Pydantic модель Activity."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} Activity>"
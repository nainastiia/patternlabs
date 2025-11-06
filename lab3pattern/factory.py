from abc import ABC, abstractmethod
from sessions import Session, Lecture, Practical
from teachers import Teacher, Lecturer, Assistant


class SessionFactory(ABC):
    """
    Abstract Creator in the Factory Method pattern.
    """

    @abstractmethod
    def create_session(self, time: str, room: str, teacher: Teacher) -> Session:
        """
        Creates a session object.
        """
        pass


class LectureFactory(SessionFactory):
    """
    Concrete Creator for Lecture objects.
    """

    def create_session(self, time: str, room: str, teacher: Lecturer) -> Lecture:
        """
        Creates and returns a new instance of a Lecture.
        """
        return Lecture(time=time, room=room, teacher=teacher)


class PracticalFactory(SessionFactory):
    """
    Concrete Creator for Practical objects.
    """

    def create_session(self, time: str, room: str, teacher: Assistant) -> Practical:
        """
        Creates and returns a new instance of a Practical.
        """
        return Practical(time=time, room=room, teacher=teacher)
from abc import ABC, abstractmethod
from teachers import Teacher, Lecturer, Assistant, ExternalMentor
from sessions import (
    Session, Lecture, Practical,
    ProgrammingLecture, ProgrammingPractical,
    DatabasesLecture, DatabasesPractical,
    MathLecture, MathPractical, AbstractSubmissionFormat
)
from courses import CourseWork, ProgrammingCourseWork, MathCourseWork, DatabasesCourseWork


class SessionFactory(ABC):
    """Abstract factory for creating sessions."""

    @abstractmethod
    def create_session(self, time: str, room: str, teacher: Teacher) -> Session:
        """Create a session."""
        pass


class LectureFactory(SessionFactory):
    """Factory for creating lectures."""

    def create_session(self, time: str, room: str, teacher: Lecturer) -> Lecture:
        """Create a lecture session."""
        return Lecture(time=time, room=room, teacher=teacher)


class PracticalFactory(SessionFactory):
    """Factory for creating practicals."""

    def create_session(self, time: str, room: str, teacher: Assistant) -> Practical:
        """Create a practical session."""
        return Practical(time=time, room=room, teacher=teacher)


class CourseFactory(ABC):
    """Abstract factory for creating course components."""

    @abstractmethod
    def create_lecture(self, time: str, room: str, teacher: Lecturer) -> Session:
        """Create a lecture."""
        pass

    @abstractmethod
    def create_practical(self, time: str, room: str, teacher: Assistant) -> Session:
        """Create a practical."""
        pass

    @abstractmethod
    def create_coursework(self, supervisor: ExternalMentor, submission_format: AbstractSubmissionFormat) -> CourseWork:
        """Create a coursework."""
        pass


class ProgrammingCourseFactory(CourseFactory):
    """Factory for programming course components."""

    def __init__(self, lecture_factory: SessionFactory, practical_factory: SessionFactory):
        """Init with session factories."""
        self.lecture_factory = lecture_factory
        self.practical_factory = practical_factory

    def create_lecture(self, time, room, teacher) -> ProgrammingLecture:
        """Create programming lecture."""
        base_lecture = self.lecture_factory.create_session(time, room, teacher)
        return ProgrammingLecture(time=base_lecture.time, room=base_lecture.room, teacher=base_lecture.teacher)

    def create_practical(self, time, room, teacher) -> ProgrammingPractical:
        """Create programming practical."""
        base_practical = self.practical_factory.create_session(time, room, teacher)
        return ProgrammingPractical(time=base_practical.time, room=base_practical.room, teacher=base_practical.teacher)

    def create_coursework(self, supervisor, submission_format) -> ProgrammingCourseWork:
        """Create programming coursework."""
        return ProgrammingCourseWork(supervisor=supervisor, submission_format=submission_format)


class MathCourseFactory(CourseFactory):
    """Factory for math course components."""

    def __init__(self, lecture_factory: SessionFactory, practical_factory: SessionFactory):
        """Init with session factories."""
        self.lecture_factory = lecture_factory
        self.practical_factory = practical_factory

    def create_lecture(self, time, room, teacher) -> MathLecture:
        """Create math lecture."""
        base_lecture = self.lecture_factory.create_session(time, room, teacher)
        return MathLecture(time=base_lecture.time, room=base_lecture.room, teacher=base_lecture.teacher)

    def create_practical(self, time, room, teacher) -> MathPractical:
        """Create math practical."""
        base_practical = self.practical_factory.create_session(time, room, teacher)
        return MathPractical(time=base_practical.time, room=base_practical.room, teacher=base_practical.teacher)

    def create_coursework(self, supervisor, submission_format) -> MathCourseWork:
        """Create math coursework."""
        return MathCourseWork(supervisor=supervisor, submission_format=submission_format)


class DatabasesCourseFactory(CourseFactory):
    """Factory for databases course components."""

    def __init__(self, lecture_factory: SessionFactory, practical_factory: SessionFactory):
        """Init with session factories."""
        self.lecture_factory = lecture_factory
        self.practical_factory = practical_factory

    def create_lecture(self, time, room, teacher) -> DatabasesLecture:
        """Create databases lecture."""
        base_lecture = self.lecture_factory.create_session(time, room, teacher)
        return DatabasesLecture(time=base_lecture.time, room=base_lecture.room, teacher=base_lecture.teacher)

    def create_practical(self, time, room, teacher) -> DatabasesPractical:
        """Create databases practical."""
        base_practical = self.practical_factory.create_session(time, room, teacher)
        return DatabasesPractical(time=base_practical.time, room=base_practical.room, teacher=base_practical.teacher)

    def create_coursework(self, supervisor, submission_format) -> DatabasesCourseWork:
        """Create databases coursework."""
        return DatabasesCourseWork(supervisor=supervisor, submission_format=submission_format)

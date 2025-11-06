from abc import abstractmethod, ABC
from teachers import Teacher, Lecturer, Assistant


class AbstractSubmissionFormat(ABC):
    """Base class for all submission formats."""

    @abstractmethod
    def process_submission(self, data: str):
        """Process submitted data."""
        pass


class OnlineUploadSubmission(AbstractSubmissionFormat):
    """Handles online file uploads."""

    def process_submission(self, file_path: str):
        """Process uploaded file."""
        print(f"Processing online upload for file: {file_path}")
        return True


class GitHubSubmission(AbstractSubmissionFormat):
    """Handles submissions via GitHub repositories."""

    def process_submission(self, repo_link: str):
        """Process GitHub repo submission."""
        print(f"Cloning and checking repository: {repo_link}")
        return True


class Session(ABC):
    """Abstract base class for course sessions."""

    def __init__(self, time: str, room: str, teacher: Teacher):
        """Initialize session with time, room, and teacher."""
        self.time = time
        self.room = room
        self.teacher = teacher

    @abstractmethod
    def perform(self):
        """Perform the session activity."""
        pass

    def __repr__(self):
        """Return session info as string."""
        return (f"{self.__class__.__name__}(Time: {self.time},"
                f" Room: {self.room}, Teacher: {self.teacher.name})")


class Lecture(Session):
    """Represents a lecture session."""

    def __init__(self, time: str, room: str, teacher: Lecturer):
        """Ensure the teacher is a Lecturer."""
        if not isinstance(teacher, Lecturer):
            raise TypeError(
                f"Lecture requires Lecturer, got {type(teacher).__name__}."
            )
        super().__init__(time, room, teacher)

    def perform(self):
        """Simulate a lecture."""
        return f"Lecturer {self.teacher.name} is reading a lecture at {self.time}."


class Practical(Session):
    """Represents a practical session."""

    def __init__(self, time: str, room: str, teacher: Assistant):
        """Initialize with an Assistant."""
        super().__init__(time, room, teacher)

    def perform(self):
        """Simulate a practical class."""
        return f"Assistant {self.teacher.name} is running a practical class at {self.time}."


class ProgrammingLecture(Lecture):
    """Programming course lecture."""
    pass


class ProgrammingPractical(Practical):
    """Programming course practical."""
    pass


class MathLecture(Lecture):
    """Math course lecture."""
    pass


class MathPractical(Practical):
    """Math course practical."""
    pass


class DatabasesLecture(Lecture):
    """Databases course lecture."""
    pass


class DatabasesPractical(Practical):
    """Databases course practical."""
    pass

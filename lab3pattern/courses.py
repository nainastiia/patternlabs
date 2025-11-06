from abc import ABC, abstractmethod
from teachers import ExternalMentor
from sessions import AbstractSubmissionFormat


class CourseWork(ABC):
    """Abstract base class for course works."""

    def __init__(self, supervisor: ExternalMentor, submission_format: AbstractSubmissionFormat):
        """Initialize with supervisor and submission format."""
        self.supervisor = supervisor
        self.submission_format = submission_format

    @abstractmethod
    def submit(self, data: str):
        """Submit coursework using a specific format."""
        pass


class ProgrammingCourseWork(CourseWork):
    """Course work for programming course."""

    def submit(self, repo_link: str):
        """Submit via GitHub repository."""
        print(f"Programming coursework submission supervised by {self.supervisor.name}")
        return self.submission_format.process_submission(repo_link)


class DatabasesCourseWork(CourseWork):
    """Course work for databases course."""

    def submit(self, file_path: str):
        """Submit via file upload."""
        print(f"Database coursework submission supervised by {self.supervisor.name}")
        return self.submission_format.process_submission(file_path)


class MathCourseWork(CourseWork):
    """Course work for math course."""

    def submit(self, file_path: str):
        """Submit via file upload."""
        print(f"Math coursework submission supervised by {self.supervisor.name}")
        return self.submission_format.process_submission(file_path)


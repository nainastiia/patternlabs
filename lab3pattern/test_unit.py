import pytest
from teachers import Lecturer, Assistant, ExternalMentor
from sessions import (
    Lecture,
    Practical,
    GitHubSubmission,
    OnlineUploadSubmission,
)
from abstract_factory import (
    LectureFactory,
    PracticalFactory,
    ProgrammingCourseFactory,
    DatabasesCourseFactory,
)
from courses import ProgrammingCourseWork, DatabasesCourseWork


# ---------- FIXTURES ----------
@pytest.fixture
def lecturer_anna():
    """Fixture for lecturer instance."""
    return Lecturer(name="Anna")

@pytest.fixture
def assistant_ivan():
    """Fixture for assistant instance."""
    return Assistant(name="Ivan")

@pytest.fixture
def mentor_olga():
    """Fixture for external mentor instance."""
    return ExternalMentor(name="Olga")

@pytest.fixture
def lecture_factory(lecturer_anna):
    """Fixture for lecture factory."""
    return LectureFactory()

@pytest.fixture
def practical_factory(assistant_ivan):
    """Fixture for practical factory."""
    return PracticalFactory()

@pytest.fixture
def programming_factory(lecture_factory, practical_factory):
    """Fixture for programming course factory."""
    return ProgrammingCourseFactory(lecture_factory, practical_factory)

@pytest.fixture
def databases_factory(lecture_factory, practical_factory):
    """Fixture for databases course factory."""
    return DatabasesCourseFactory(lecture_factory, practical_factory)

@pytest.fixture
def github_format():
    """Fixture for GitHub submission format."""
    return GitHubSubmission()

@pytest.fixture
def online_format():
    """Fixture for online upload submission format."""
    return OnlineUploadSubmission()


# ---------- UNIT TESTS ----------
class TestFactoryMethods:
    """Tests for simple factory classes."""

    def test_lecture_factory_creates_lecture_session(self, lecture_factory, lecturer_anna):
        """LectureFactory should create a Lecture with correct teacher."""
        session = lecture_factory.create_session("Mon 10:00", "301", lecturer_anna)
        assert isinstance(session, Lecture)
        assert session.teacher == lecturer_anna

    def test_practical_factory_creates_practical_session(self, practical_factory, assistant_ivan):
        """PracticalFactory should create a Practical with correct teacher."""
        session = practical_factory.create_session("Tue 11:30", "105", assistant_ivan)
        assert isinstance(session, Practical)
        assert session.teacher == assistant_ivan


class TestAbstractFactory:
    """Tests for abstract factories creating full course components."""

    def test_programming_factory_creates_correct_types(
        self, programming_factory, lecturer_anna, assistant_ivan, mentor_olga, github_format
    ):
        """ProgrammingCourseFactory creates lecture, practical, and coursework of correct types."""
        lecture = programming_factory.create_lecture("Wed 10:00", "401", lecturer_anna)
        practical = programming_factory.create_practical("Wed 11:45", "101", assistant_ivan)
        coursework = programming_factory.create_coursework(mentor_olga, github_format)

        assert 'ProgrammingLecture' in lecture.__class__.__name__
        assert 'ProgrammingPractical' in practical.__class__.__name__
        assert isinstance(coursework, ProgrammingCourseWork)

    def test_databases_factory_creates_databases_coursework(
        self, databases_factory, mentor_olga, online_format
    ):
        """DatabasesCourseFactory creates DatabasesCourseWork."""
        coursework = databases_factory.create_coursework(mentor_olga, online_format)
        assert isinstance(coursework, DatabasesCourseWork)
        assert coursework.supervisor == mentor_olga


class TestTeacherConstraints:
    """Tests for type constraints on teachers."""

    def test_lecturer_can_be_assigned_to_lecture(self, lecturer_anna):
        """Lecturer should be valid for Lecture."""
        try:
            Lecture("Mon 10:00", "301", lecturer_anna)
        except TypeError:
            pytest.fail("Lecturer should be able to be assigned to a Lecture.")

    def test_external_mentor_cannot_be_assigned_to_lecture(self, mentor_olga):
        """ExternalMentor should not be valid for Lecture."""
        with pytest.raises(TypeError) as excinfo:
            Lecture("Mon 10:00", "301", mentor_olga)
        assert "Lecture requires Lecturer, got ExternalMentor." in str(excinfo.value)



class TestCourseWorkSubmission:
    """Tests for coursework submission processing."""

    def test_online_submission_processing_output(self, mentor_olga, online_format, capsys):
        """OnlineUploadSubmission should print correct output."""
        coursework = DatabasesCourseWork(mentor_olga, online_format)
        coursework.submit("/tmp/design.pdf")
        captured = capsys.readouterr()

        assert "Database coursework submission supervised by Olga" in captured.out
        assert "Processing online upload for file: /tmp/design.pdf" in captured.out

    def test_github_submission_processing_output(self, mentor_olga, github_format, capsys):
        """GitHubSubmission should print correct output."""
        coursework = ProgrammingCourseWork(mentor_olga, github_format)
        coursework.submit("https://github.com/my/repo")
        captured = capsys.readouterr()

        assert "Programming coursework submission supervised by Olga" in captured.out
        assert "Cloning and checking repository: https://github.com/my/repo" in captured.out


import pytest
from teachers import Lecturer, Assistant, ExternalMentor
from groups import StudentGroup
from abstract_factory import ProgrammingCourseFactory, DatabasesCourseFactory, LectureFactory, PracticalFactory
from sessions import GitHubSubmission, OnlineUploadSubmission
from courses import ProgrammingCourseWork


# ---------- FIXTURES ----------

@pytest.fixture
def lecturer_anna():
    """Return a Lecturer instance named Anna."""
    return Lecturer(name="Anna")


@pytest.fixture
def assistant_ivan():
    """Return an Assistant instance named Ivan."""
    return Assistant(name="Ivan")


@pytest.fixture
def mentor_olga():
    """Return an ExternalMentor instance named Olga."""
    return ExternalMentor(name="Olga")


@pytest.fixture
def group_fep23():
    """Return a new student group named FEP-23."""
    return StudentGroup(name="FEP-23")


@pytest.fixture
def lecture_factory():
    """Return a base LectureFactory instance."""
    return LectureFactory()


@pytest.fixture
def practical_factory():
    """Return a base PracticalFactory instance."""
    return PracticalFactory()


@pytest.fixture
def programming_factory(lecture_factory, practical_factory):
    """Return a ProgrammingCourseFactory using lecture and practical factories."""
    return ProgrammingCourseFactory(lecture_factory, practical_factory)


@pytest.fixture
def databases_factory(lecture_factory, practical_factory):
    """Return a DatabasesCourseFactory using lecture and practical factories."""
    return DatabasesCourseFactory(lecture_factory, practical_factory)


@pytest.fixture
def github_format():
    """Return a GitHub submission format instance."""
    return GitHubSubmission()


@pytest.fixture
def online_format():
    """Return an Online upload submission format instance."""
    return OnlineUploadSubmission()


# ---------- INTEGRATION TESTS ----------

class TestGroupEnrollmentIntegration:
    """Integration tests verifying enrollment, scheduling, and teacher validation."""

    def test_group_enrollment_adds_both_sessions(
        self, group_fep23, programming_factory, lecturer_anna, assistant_ivan,
        mentor_olga, github_format
    ):
        """Check that enrolling a course adds lecture and practical sessions."""
        initial_schedule_count = len(group_fep23.schedule)

        coursework = group_fep23.enroll_course(
            factory=programming_factory,
            lecture_time="Mon 10:00",
            practical_time="Mon 11:45",
            room="301",
            lecturer=lecturer_anna,
            assistant=assistant_ivan,
            mentor=mentor_olga,
            submission_format=github_format
        )

        assert len(group_fep23.schedule) == initial_schedule_count + 2
        assert isinstance(coursework, ProgrammingCourseWork)

    def test_consistent_course_creation_check(
        self, group_fep23, databases_factory, lecturer_anna,
        assistant_ivan, mentor_olga, online_format
    ):
        """Ensure created sessions match course type and assigned teachers."""
        initial_len = len(group_fep23.schedule)

        group_fep23.enroll_course(
            factory=databases_factory,
            lecture_time="Tue 10:00",
            practical_time="Tue 11:45",
            room="205",
            lecturer=lecturer_anna,
            assistant=assistant_ivan,
            mentor=mentor_olga,
            submission_format=online_format
        )

        lecture = group_fep23.schedule[initial_len]
        practical = group_fep23.schedule[initial_len + 1]

        assert 'DatabasesLecture' in lecture.__class__.__name__
        assert 'DatabasesPractical' in practical.__class__.__name__
        assert lecture.teacher == lecturer_anna
        assert practical.teacher == assistant_ivan

    def test_scheduling_conflicts_detection(
        self, group_fep23, programming_factory, databases_factory,
        lecturer_anna, assistant_ivan, mentor_olga, github_format
    ):
        """Detect time conflicts between sessions in the group schedule."""
        group_fep23.enroll_course(
            factory=programming_factory,
            lecture_time="Mon 10:00",
            practical_time="Mon 11:45",
            room="301",
            lecturer=lecturer_anna,
            assistant=assistant_ivan,
            mentor=mentor_olga,
            submission_format=github_format
        )

        group_fep23.enroll_course(
            factory=databases_factory,
            lecture_time="Mon 10:00",  # same time, should conflict
            practical_time="Tue 11:45",
            room="205",
            lecturer=lecturer_anna,
            assistant=assistant_ivan,
            mentor=mentor_olga,
            submission_format=github_format
        )

        conflicts = group_fep23.check_conflicts()

        assert len(conflicts) == 1
        session1, session2 = conflicts[0]
        assert session1.time == "Mon 10:00"

    def test_teacher_restriction_enforcement_on_enrollment(
        self, group_fep23, programming_factory, assistant_ivan,
        mentor_olga, github_format
    ):
        """Verify that incorrect teacher types raise TypeError during enrollment."""
        with pytest.raises(TypeError) as excinfo:
            group_fep23.enroll_course(
                factory=programming_factory,
                lecture_time="Wed 10:00",
                practical_time="Wed 11:45",
                room="301",
                lecturer=mentor_olga,  # wrong type
                assistant=assistant_ivan,
                mentor=mentor_olga,
                submission_format=github_format
            )

        assert str(excinfo.value) == "Lecture requires Lecturer, got ExternalMentor."
        assert len(group_fep23.schedule) == 0


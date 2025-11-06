from typing import List
from sessions import Session
from abstract_factory import CourseFactory
from teachers import Lecturer, Assistant, ExternalMentor


class StudentGroup:
    """Represents a student group with a schedule."""

    def __init__(self, name: str):
        """Initialize group with name and empty schedule."""
        self.name = name
        self.schedule: List[Session] = []

    def add_session(self, session: Session):
        """Add a session to the schedule."""
        self.schedule.append(session)

    def enroll_course(
        self,
        factory: CourseFactory,
        lecture_time: str,
        practical_time: str,
        room: str,
        lecturer: Lecturer,
        assistant: Assistant,
        mentor: ExternalMentor,
        submission_format,
    ):
        """Enroll the group in a course using the provided factory."""
        lecture = factory.create_lecture(lecture_time, room, lecturer)
        practical = factory.create_practical(practical_time, room, assistant)
        coursework = factory.create_coursework(mentor, submission_format)

        self.add_session(lecture)
        self.add_session(practical)

        return coursework

    def check_conflicts(self) -> List[tuple]:
        """Check for time conflicts between sessions."""
        conflicts = []
        time_slots = {}

        for session in self.schedule:
            time = session.time
            if time in time_slots:
                conflicts.append((session, time_slots[time]))
            else:
                time_slots[time] = session

        return conflicts


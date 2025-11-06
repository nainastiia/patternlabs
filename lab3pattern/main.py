from teachers import Lecturer, Assistant, ExternalMentor
from abstract_factory import LectureFactory, PracticalFactory, ProgrammingCourseFactory, MathCourseFactory, DatabasesCourseFactory
from sessions import GitHubSubmission, OnlineUploadSubmission
from groups import StudentGroup

def main():
    # Create teachers and mentors
    lecturer_programming = Lecturer("Anna")
    assistant_programming = Assistant("Ivan")
    mentor_programming = ExternalMentor("Olga")

    lecturer_math = Lecturer("Bogdan")
    assistant_math = Assistant("Maria")
    mentor_math = ExternalMentor("Svitlana")

    lecturer_db = Lecturer("Alexander")
    assistant_db = Assistant("Katerina")
    mentor_db = ExternalMentor("Igor")

    #  Create session factories
    lecture_factory = LectureFactory()
    practical_factory = PracticalFactory()

    #  Create course factories
    programming_factory = ProgrammingCourseFactory(lecture_factory, practical_factory)
    math_factory = MathCourseFactory(lecture_factory, practical_factory)
    databases_factory = DatabasesCourseFactory(lecture_factory, practical_factory)

    # Create a student group
    group_fep23 = StudentGroup("FEP-23")

    #  Enroll the group in Programming course
    programming_coursework = group_fep23.enroll_course(
        factory=programming_factory,
        lecture_time="Mon 10:00",
        practical_time="Mon 11:45",
        room="301",
        lecturer=lecturer_programming,
        assistant=assistant_programming,
        mentor=mentor_programming,
        submission_format=GitHubSubmission()
    )

    #  Enroll the group in Math course
    math_coursework = group_fep23.enroll_course(
        factory=math_factory,
        lecture_time="Tue 10:00",
        practical_time="Tue 11:45",
        room="205",
        lecturer=lecturer_math,
        assistant=assistant_math,
        mentor=mentor_math,
        submission_format=OnlineUploadSubmission()
    )

    # Enroll the group in Databases course
    databases_coursework = group_fep23.enroll_course(
        factory=databases_factory,
        lecture_time="Wed 10:00",
        practical_time="Wed 11:45",
        room="402",
        lecturer=lecturer_db,
        assistant=assistant_db,
        mentor=mentor_db,
        submission_format=OnlineUploadSubmission()
    )

    #  Print group schedule
    print("\nSchedule of group FEP-23:")
    for session in group_fep23.schedule:
        print(session.perform())

    #  Submit coursework
    print("\nCoursework submission:")
    programming_coursework.submit("https://github.com/my/repo")
    math_coursework.submit("/tmp/math_homework.pdf")
    databases_coursework.submit("/tmp/databases_homework.pdf")

    # Check for schedule conflicts
    conflicts = group_fep23.check_conflicts()
    if conflicts:
        print("\nSchedule conflicts detected")
        for s1, s2 in conflicts:
            print(f"Conflict: {s1} and {s2}")
    else:
        print("\nNo conflicts in the schedule.")

if __name__ == "__main__":
    main()

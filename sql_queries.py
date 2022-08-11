from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

from orm_sqlalchemy.models import Group, association_table, Student, Course

from dotenv import load_dotenv
import os

load_dotenv()


def find_groups_by_students_count(Session, count):
    """Find all groups with less or equals student count."""
    with Session() as session:
        groups_counted = session.query(Group.id, Group.name, func.count(Student.group_id).label('n_students')) \
            .join(Student).group_by(Group.id).having(func.count(Student.group_id) <= count).all()
    return groups_counted


def students_on_course(Session, coursename):
    """Find all students related to the course with a given name."""
    with Session() as session:
        students_lst = session.query(Student.first_name, Student.last_name).join(association_table).join(Course) \
            .filter(Course.name == coursename).all()
    return students_lst


def add_new_student(Session, first_name, last_name, group_id, courses_ids):
    """Add a new student"""
    with Session() as session:
        max_id = session.query(func.max(Student.id)).scalar()
        new_student = Student(id=max_id + 1, first_name=first_name, last_name=last_name, group_id=group_id,
                              courses=[session.query(Course).get(course_id) for course_id in courses_ids])
        session.add(new_student)
        session.commit()
        print("-" * 70)
        print("New student added:", new_student.first_name, new_student.last_name)


def remove_student(Session, the_id):
    """Delete student by STUDENT_ID"""
    with Session() as session:
        the_student = session.query(Student).get(the_id)
        student_courses = the_student.courses
        for course in student_courses:
            course.students.remove(the_student)
        session.delete(the_student)
        session.commit()
        print("-" * 70)
        print(f"Student with id {the_id} successfully removed")


def add_student_to_course(Session, student_id, course_id):
    """Add a student to the course (from a list)"""
    with Session() as session:
        the_course = session.query(Course).get(course_id)
        the_student = session.query(Student).get(student_id)
        the_course.students.append(the_student)
        session.commit()
        print("-" * 70)
        print(f"Student {the_student} added to course {the_course}")
        print(f"This student's courses are:{the_student.courses}")


def remove_student_from_course(Session, student_id, course_id):
    """Remove the student from one of his or her courses"""
    with Session() as session:
        the_student = session.query(Student).get(student_id)
        the_course = session.query(Course).get(course_id)
        the_course.students.remove(the_student)
        session.commit()
        print("-" * 70)
        print(f"Student {the_student} removed from course {the_course}")
        print(f"This student's courses are:{the_student.courses}")


if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            os.environ.get('DB_USERNAME'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT'),
            os.environ.get('DB_NAME'),
        ), echo=True)

    Session = sessionmaker(bind=engine)
    groups_counted = find_groups_by_students_count(Session, 21)
    print("-" * 70)
    print(f"groups with <=21 students:")
    print(groups_counted)

    students_lst = students_on_course("Discrete Math")
    print("-" * 70)
    print(f"students on Discrete Math course:")
    print(students_lst)

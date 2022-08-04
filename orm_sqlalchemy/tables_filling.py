from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random

from models import Group, association_table, Student, Course
from generator_source import group_names, course_names
from generating_data import assign_to_groups

engine = create_engine('postgresql+psycopg2://postgres:default@localhost:5432/university_db', echo=True)

Session = sessionmaker(bind=engine)

groups_dict = assign_to_groups()  # assigning students to groups


def fill_groups():
    with Session() as session:
        session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names, 1)])
        session.commit()


def fill_courses():
    with Session() as session:
        session.add_all(
            [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names, 1)])
        session.commit()


def fill_students():
    with Session() as session:
        i = 0
        for group_number, groupname in enumerate(groups_dict.keys(), 1):
            for student in groups_dict[groupname]:
                courses = set(random.sample(range(1, 10), random.choice([1, 2, 3])))
                session.add(Student(id=i + 1, first_name=student[0], last_name=student[1], group_id=group_number,
                                    courses=[session.query(Course).get(course_id) for course_id in courses]))
                i += 1

        session.commit()


if __name__ == '__main__':
    fill_groups()
    fill_courses()
    fill_students()
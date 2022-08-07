import pytest

from sql_queries import *
from orm_sqlalchemy.models import Base, Group, association_table, Student, Course
from orm_sqlalchemy.generator_source import group_names, course_names


def seed_database():
    with Session(bind=connection) as session:
        session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])

        session.commit()

        session.add_all(
            [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
        session.commit()

        groups_dict = {"FI-83":
                           [['Alice', 'Evans', [1]], ['Helen', 'Turner', [2, 4]], ['Jack', 'Fox', [1, 3]],
                            ['Leo', 'Fisher', [3]]],
                       "FB-61":
                           [['Andrew', 'Turner', [2, 3]], ['Jane', 'Garfield', [1, 3, 4]], ['Harry', 'Styles', [4]]],
                       "SA-72":
                           [['Alan', 'Turing', [1, 2, 3]], ['Sophia', 'Roberts', [1, 4]]]}

        i = 0
        for group_number, groupname in enumerate(groups_dict.keys(), 1):
            for student in groups_dict[groupname]:
                courses = student[2]
                session.add(Student(id=i + 1, first_name=student[0], last_name=student[1], group_id=group_number,
                                    courses=[session.query(Course).get(course_id) for course_id in courses]))
                i += 1

        session.commit()


# @pytest.fixture
# def the_session():
#     engine = create_engine("postgresql+psycopg2://postgres:default@localhost:5432/test_university_db")
#     connection = engine.connect()
#     Base.metadata.bind = connection
#     # Base.metadata.create_all()
#     session = Session(bind=connection)
#     yield session
#
#     session.close()
#     connection.close()
#     Base.metadata.drop_all()


# def setup_db(the_session):
#     # seed_database()
#     with the_session as session:
#         session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
#
#         session.commit()
#
#         session.add_all(
#             [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
#         session.commit()
#
#         groups_dict = {"FI-83":
#                            [['Alice', 'Evans', [1]], ['Helen', 'Turner', [2, 4]], ['Jack', 'Fox', [1, 3]],
#                             ['Leo', 'Fisher', [3]]],
#                        "FB-61":
#                            [['Andrew', 'Turner', [2, 3]], ['Jane', 'Garfield', [1, 3, 4]], ['Harry', 'Styles', [4]]],
#                        "SA-72":
#                            [['Alan', 'Turing', [1, 2, 3]], ['Sophia', 'Roberts', [1, 4]]]}
#
#         i = 0
#         for group_number, groupname in enumerate(groups_dict.keys(), 1):
#             for student in groups_dict[groupname]:
#                 courses = student[2]
#                 session.add(Student(id=i + 1, first_name=student[0], last_name=student[1], group_id=group_number,
#                                     courses=[session.query(Course).get(course_id) for course_id in courses]))
#                 i += 1
#
#         session.commit()

engine = create_engine("postgresql+psycopg2://postgres:default@localhost:5432/test_university_db")
connection = engine.connect()
Base.metadata.bind = connection
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
seed_database()

def test_find_groups_by_students_count():
    count = 3
    groups_counted = find_groups_by_students_count(Session, count)
    assert groups_counted == [("FB-61", 3), ("SA-72", 2)]

def test_students_on_course():
    number = students_on_course(Session, "Discrete Math")
    assert number == [('Alice', 'Evans'), ('Jack', 'Fox'), ('Jane', 'Garfield'), ('Alan', 'Turing'),
                      ('Sophia', 'Roberts')]

def test_add_new_student():
    add_new_student(Session, first_name="Steve", last_name="Rogers", group_id=3, courses_ids=[4])
    with Session() as session:
        newstudent = session.query(Student).filter_by(first_name="Steve", last_name="Rogers").first()
    assert str(newstudent) == 'Student(id=10, group=3, first_name=Steve, last_name=Rogers)'

def test_add_student_to_course():
    add_student_to_course(Session, 10, 1)
    with Session() as session:
        steve = session.query(Student).filter_by(first_name="Steve", last_name="Rogers").first()
        discr_math = session.query(Course).filter_by(id=1).first()
        print("discr_math.students=", discr_math.students)
        assert steve in discr_math.students

def test_remove_student_from_course():
    remove_student_from_course(Session, 10, 1)
    with Session() as session:
        steve = session.query(Student).filter_by(first_name="Steve", last_name="Rogers").first()
        discr_math = session.query(Course).filter_by(id=1).first()
        print("discr_math.students=", discr_math.students)
        assert steve not in discr_math.students

def test_remove_student():
    remove_student(Session, 10)
    with Session() as session:
        n_steves = session.query(Student).filter_by(first_name="Steve", last_name="Rogers").count()
        assert n_steves == 0

# Base.metadata.drop_all()
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from sql_queries import *
from orm_sqlalchemy.models import Base, Group, association_table, Student, Course
from orm_sqlalchemy.generator_source import group_names, course_names


@pytest.fixture(scope="session")
def connection():
    print("\nCONNECTING\n")
    engine = create_engine("postgresql+psycopg2://postgres:default@localhost:5433/test_university_db")
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    seed_database()

    yield

    Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


def seed_database():

    db_session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
    db_session.commit()

    db_session.add_all(
        [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
    db_session.commit()

    groups_dict = {"FI-83":
                   [['Alice', 'Evans',[1]], ['Helen', 'Turner',[2,4]], ['Jack', 'Fox',[1,3]], ['Leo', 'Fisher',[3]]],
                   "FB-61":
                   [['Andrew', 'Turner',[2,3]], ['Jane', 'Garfield',[1,3,4]], ['Harry', 'Styles',[4]]],
                   "SA-72":
                   [['Alan', 'Turing',[1,2,3]], ['Sophia', 'Roberts', [1,4]]]}

    i = 0
    for group_number, groupname in enumerate(groups_dict.keys(), 1):
        for student in groups_dict[groupname]:
            courses = student[2]
            db_session.add(Student(id=i + 1, first_name=student[0], last_name=student[1], group_id=group_number,
                                courses=[db_session.query(Course).get(course_id) for course_id in courses]))
    db_session.commit()


def test_find_groups_by_students_count(db_session):
    print("\nCOUNTING GROUPS\n")
    groups_counted = find_groups_by_students_count(3)
    assert groups_counted == [("FB-61", 3), ("SA-72", 2)]
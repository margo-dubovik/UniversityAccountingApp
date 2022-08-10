import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_sqlalchemy.generator_source import group_names, course_names
from orm_sqlalchemy.models import Base, Group, Student, Course


@pytest.fixture(scope='session')
def engine():
    engine = create_engine("postgresql+psycopg2://postgres:default@localhost:5432/test_university_db")
    yield engine


@pytest.fixture(scope='session')
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='session')
def session(connection):
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))
    yield Session
    Session.close()


@pytest.fixture(scope='function')
def testdb(connection, engine, session):
    Base.metadata.bind = connection
    Base.metadata.create_all(engine)

    with session() as session:
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

    yield testdb

    Base.metadata.drop_all()

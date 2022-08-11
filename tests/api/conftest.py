import pytest

import university_accounting_api

from orm_sqlalchemy.generator_source import group_names, course_names

from dotenv import load_dotenv
import os

load_dotenv()

groups_dict = {"FI-83":
                   [['Alice', 'Evans', [1]], ['Helen', 'Turner', [2, 4]], ['Jack', 'Fox', [1, 3]],
                    ['Leo', 'Fisher', [3]]],
               "FB-61":
                   [['Andrew', 'Turner', [2, 3]], ['Jane', 'Garfield', [1, 3, 4]], ['Harry', 'Styles', [4]]],
               "SA-72":
                   [['Alan', 'Turing', [1, 2, 3]], ['Sophia', 'Roberts', [1, 4]]]}


@pytest.fixture(scope='session')
def app():
    db_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ.get('TEST_DB_USERNAME'),
        os.environ.get('TEST_DB_PASSWORD'),
        os.environ.get('TEST_DB_HOST'),
        os.environ.get('TEST_DB_PORT'),
        os.environ.get('TEST_DB_NAME'),
    )
    university_accounting_api.app.config['TESTING'] = True
    university_accounting_api.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    yield university_accounting_api.app


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope='function')
def testdb(app):
    from university_accounting import db
    print("\ndb=", db)
    db.drop_all()
    db.create_all()
    print("Tables created:")
    for t in db.metadata.tables.items():
        print("table ", t)

    yield db
    print("\nsession.remove called")
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='session')
def testdb_filled(app):
    from university_accounting import db, Group, Student, Course
    print("\ndb=", db)
    db.drop_all()
    db.create_all()
    print("Tables created:")
    for t in db.metadata.tables.items():
        print("table ", t)

    db.session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
    db.session.flush()

    db.session.add_all(
        [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
    db.session.flush()

    i = 0
    for group_number, groupname in enumerate(groups_dict.keys(), 1):
        for student in groups_dict[groupname]:
            courses = student[2]
            db.session.add(Student(id=i + 1, first_name=student[0], last_name=student[1], group_id=group_number,
                                   courses=[db.session.query(Course).get(course_id) for course_id in courses]))
            i += 1
    db.session.commit()

    yield db

    print("\nsession.remove called")
    db.session.remove()
    db.drop_all()

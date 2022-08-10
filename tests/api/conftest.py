import pytest

from flask_sqlalchemy import SQLAlchemy

import university_accounting_api

# from university_accounting import Group, association_table, Student, Course, courses_dict
from orm_sqlalchemy.generator_source import group_names, course_names

groups_dict = {"FI-83":
                   [['Alice', 'Evans', [1]], ['Helen', 'Turner', [2, 4]], ['Jack', 'Fox', [1, 3]],
                    ['Leo', 'Fisher', [3]]],
               "FB-61":
                   [['Andrew', 'Turner', [2, 3]], ['Jane', 'Garfield', [1, 3, 4]], ['Harry', 'Styles', [4]]],
               "SA-72":
                   [['Alan', 'Turing', [1, 2, 3]], ['Sophia', 'Roberts', [1, 4]]]}

@pytest.fixture(scope='session')
def app():
    db_uri = "postgresql+psycopg2://postgres:default@localhost:5432/test_university_db"
    university_accounting_api.app.config['TESTING'] = True
    university_accounting_api.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    yield university_accounting_api.app


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope='function')
def testdb(app):
    db = SQLAlchemy(app)

    print("\ndb connected")

    class Group(db.Model):
        __tablename__ = "groups"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(5))

        students = db.relationship("Student", backref='groups')

        def __repr__(self):
            return f"Group(id={self.id}, name={self.name})"

    association_table = db.Table(
        "association",
        db.Column("student_id", db.ForeignKey("students.id"), primary_key=True),
        db.Column("course_id", db.ForeignKey("courses.id"), primary_key=True),
    )

    class Student(db.Model):
        __tablename__ = "students"

        id = db.Column(db.Integer, primary_key=True)
        group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)

        courses = db.relationship(
            "Course", secondary=association_table, backref="students"
        )

        def __repr__(self):
            return f"Student(id={self.id}, group_id={self.group_id}, first_name={self.first_name}, last_name={self.last_name})"

    class Course(db.Model):
        __tablename__ = "courses"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(250), nullable=False)

        def __repr__(self):
            return f"Course(id={self.id}, name={self.name}, description={self.description})"

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
    db = SQLAlchemy(app)

    print("\ndb connected")

    class Group(db.Model):
        __tablename__ = "groups"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(5))

        students = db.relationship("Student", backref='groups')

        def __repr__(self):
            return f"Group(id={self.id}, name={self.name})"

    association_table = db.Table(
        "association",
        db.Column("student_id", db.ForeignKey("students.id"), primary_key=True),
        db.Column("course_id", db.ForeignKey("courses.id"), primary_key=True),
    )

    class Student(db.Model):
        __tablename__ = "students"

        id = db.Column(db.Integer, primary_key=True)
        group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)

        courses = db.relationship(
            "Course", secondary=association_table, backref="students"
        )

        def __repr__(self):
            return f"Student(id={self.id}, group_id={self.group_id}, first_name={self.first_name}, last_name={self.last_name})"

    class Course(db.Model):
        __tablename__ = "courses"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(250), nullable=False)

        def __repr__(self):
            return f"Course(id={self.id}, name={self.name}, description={self.description})"

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

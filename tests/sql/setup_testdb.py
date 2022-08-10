from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm_sqlalchemy.generator_source import group_names, course_names
from orm_sqlalchemy.models import Base, Group, Student, Course


def seed_database():
    with Session() as session:
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


engine = create_engine("postgresql+psycopg2://postgres:default@localhost:5432/test_university_db")
connection = engine.connect()
Base.metadata.bind = connection
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
# seed_database()

# Base.metadata.drop_all()
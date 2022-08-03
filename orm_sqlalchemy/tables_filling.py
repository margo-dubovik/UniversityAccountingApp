from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Group, association_table, Student, Course

from generator_source import group_names, course_names
from generating_data import assign_to_groups

engine = create_engine('postgresql+psycopg2://postgres:default@localhost:5432/university_db', echo=True)

Session = sessionmaker(bind=engine)

groups_dict = assign_to_groups()  # assigning students to groups

with Session() as session:
    session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names, 1)])
    session.commit()

    session.add_all([Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names, 1)])
    session.commit()

    i=0
    for groupname in groups_dict.keys():
        for student in groups_dict[groupname]:
            session.add([Student(id=i+1, first_name=student[0], last_name=student[1], group_id=" ??? ", courses="???")])
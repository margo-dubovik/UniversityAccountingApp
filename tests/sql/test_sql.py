from sql_queries import *
from orm_sqlalchemy.models import Student, Course

from tests.sql.setup_testdb import Session



def test_find_groups_by_students_count():
    count = 3
    groups_counted = find_groups_by_students_count(Session, count)
    assert groups_counted == [(2, "FB-61", 3), (3, "SA-72", 2)]

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

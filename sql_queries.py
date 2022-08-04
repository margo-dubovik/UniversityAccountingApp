from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func, select, subquery

from orm_sqlalchemy.models import Group, association_table, Student, Course

engine = create_engine('postgresql+psycopg2://postgres:default@localhost:5432/university_db', echo=True)

Session = sessionmaker(bind=engine)


# Find all groups with less or equals student count.
def find_by_count(count):
    with Session() as session:
        subq = select(Group.name, func.count(Student.group_id).label('n_students')) \
            .join(Student).group_by(Group.id).subquery()
        students_counted = session.query(subq).filter(subq.c.n_students <= count).all()
    print(students_counted)


# Find all students related to the course with a given name.
def students_on_course(coursename):
    with Session() as session:
        students_lst = session.query(Student.first_name,Student.last_name).join(association_table).join(Course)\
            .filter(Course.name == coursename).all()
        print(students_lst)

# Add new student

# Delete student by STUDENT_ID

# Add a student to the course (from a list)

# Remove the student from one of his or her courses

if __name__ == '__main__':
    # find_by_count(25)
    # students_on_course("Discrete Math")


# number of students in each group:  (group № 10 is empty)
# [(8, 22), (9, 23), (7, 27), (1, 12), (5, 20), (4, 28), (2, 29), (6, 26), (3, 13)]

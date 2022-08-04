from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func, select, subquery

from orm_sqlalchemy.models import Group, association_table, Student, Course

engine = create_engine('postgresql+psycopg2://postgres:default@localhost:5432/university_db', echo=True)

Session = sessionmaker(bind=engine)


# Find all groups with less or equals student count.
def find_groups_by_students_count(count):
    with Session() as session:
        subq = select(Group.name, func.count(Student.group_id).label('n_students')) \
            .join(Student).group_by(Group.id).subquery()
        students_counted = session.query(subq).filter(subq.c.n_students <= count).all()
        print("-"*70)
        print(f"groups with <={count} students:")
        print(students_counted)


# Find all students related to the course with a given name.
def students_on_course(coursename):
    with Session() as session:
        students_lst = session.query(Student.first_name, Student.last_name).join(association_table).join(Course) \
            .filter(Course.name == coursename).all()
        print("-" * 70)
        print(f"students on {coursename} course:")
        print(students_lst)


# Add new student
def add_new_student(first_name, last_name, group_id, courses_ids):
    with Session() as session:
        max_id = session.query(func.max(Student.id)).scalar()
        new_student = Student(id=max_id + 1, first_name=first_name, last_name=last_name, group_id=group_id,
                              courses=[session.query(Course).get(course_id) for course_id in courses_ids])
        session.add(new_student)
        session.commit()
        print("-" * 70)
        print("New student added:", new_student.first_name, new_student.last_name)


# Delete student by STUDENT_ID
def remove_student(the_id):
    with Session() as session:
        the_student = session.query(Student).get(the_id)
        student_courses = the_student.courses
        # print("the_student=", the_student)
        # print("student_courses=", student_courses)
        for course in student_courses:
            # print("course=", course)
            course.students.remove(the_student)
        session.delete(the_student)
        session.commit()
        print("-" * 70)
        print(f"Student with id {the_id } successfully removed")


# Add a student to the course (from a list)
def add_student_to_course(student_id, course_id):
    with Session() as session:
        the_course = session.query(Course).get(course_id)
        the_student = session.query(Student).get(student_id)
        the_course.students.append(the_student)
        session.commit()
        print("-" * 70)
        print(f"Student {the_student} added to course {the_course}")
        print(f"This student's courses are:{the_student.courses}")


# Remove the student from one of his or her courses
def remove_student_from_course(student_id, course_id):
    with Session() as session:
        the_student = session.query(Student).get(student_id)
        student_courses = the_student.courses
        the_course = session.query(Course).get(course_id)
        the_course.students.remove(the_student)
        session.commit()
        print("-" * 70)
        print(f"Student {the_student} removed from course {the_course}")
        print(f"This student's courses are:{the_student.courses}")


if __name__ == '__main__':
    find_groups_by_students_count(21)
    students_on_course("Discrete Math")
    add_new_student(first_name="Harry", last_name="Styles", group_id=10, courses_ids=[4, 6, 7])
    add_student_to_course(201, 5)
    remove_student_from_course(201, 5)
    remove_student(201)

# number of students in each group:  (group № 10 is empty)
# [(8, 22), (9, 23), (7, 27), (1, 12), (5, 20), (4, 28), (2, 29), (6, 26), (3, 13)]

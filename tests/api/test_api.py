import json

from tests.api.varscompare import *
from university_accounting import Group, Student, Course
from orm_sqlalchemy.generator_source import group_names, course_names


def format_output(text):
    return ''.join(text.split())


groups_dict = {"FI-83":
                   [['Alice', 'Evans', [1]], ['Helen', 'Turner', [2, 4]], ['Jack', 'Fox', [1, 3]],
                    ['Leo', 'Fisher', [3]]],
               "FB-61":
                   [['Andrew', 'Turner', [2, 3]], ['Jane', 'Garfield', [1, 3, 4]], ['Harry', 'Styles', [4]]],
               "SA-72":
                   [['Alan', 'Turing', [1, 2, 3]], ['Sophia', 'Roberts', [1, 4]]]}


def test_groupsbycount(client, testdb_filled):
    response = client.get("/api/v1/groups/by_count?count=3&format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_groupsbycount

    response = client.get("/api/v1/groups/by_count?count=3&format=xml")
    assert response.status_code == 200
    assert format_output(response.get_data(as_text=True)) == format_output(xml_groupsbycount)


def test_studentsoncourse_get(client, testdb_filled):
    response = client.get("/api/v1/courses/physics/students?format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_studentsoncourse

    response = client.get("/api/v1/courses/physics/students?format=xml")
    assert response.status_code == 200
    assert format_output(response.get_data(as_text=True)) == format_output(xml_studentsoncourse)


def test_studentsoncourse_post(client, testdb):
    testdb.session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
    testdb.session.flush()

    testdb.session.add_all(
        [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
    testdb.session.flush()

    helen_courses = [1,4]
    helen = Student(id=1, first_name='Helen', last_name='Turner', group_id=1,
                    courses=[testdb.session.query(Course).get(course_id) for course_id in helen_courses])
    testdb.session.add(helen)
    testdb.session.commit()

    response = client.post("/api/v1/courses/physics/students?student_id=1&format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_studentsoncourse_post_ok

    physics = Course.query.get(2)
    helen = Student.query.get(1)
    assert helen in physics.students

    response = client.post("/api/v1/courses/physics/students?student_id=1&format=json")
    assert response.status_code == 400
    assert json.loads(response.get_data()) == json_studentsoncourse_alreadythere

def test_studentsoncourse_delete(client, testdb):
    testdb.session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
    testdb.session.flush()

    testdb.session.add_all(
        [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
    testdb.session.flush()

    helen_courses = [2, 4]
    helen = Student(id=1, first_name='Helen', last_name='Turner', group_id=1,
                    courses=[testdb.session.query(Course).get(course_id) for course_id in helen_courses])
    testdb.session.add(helen)
    alan_courses = [2, 3]
    alan = Student(id=2, first_name='Alan', last_name='Turing', group_id=3,
                    courses=[testdb.session.query(Course).get(course_id) for course_id in alan_courses])
    testdb.session.add(alan)
    testdb.session.commit()

    response = client.delete("/api/v1/courses/physics/students?student_id=1&format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_studentsoncourse_delete_ok

    physics = Course.query.get(2)
    helen = Student.query.get(1)
    assert helen not in physics.students

    response = client.delete("/api/v1/courses/physics/students?student_id=1&format=json")
    assert response.status_code == 400
    assert json.loads(response.get_data()) == json_studentsoncourse_notin


def test_studentsoperations_get(client, testdb):
    testdb.session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
    testdb.session.flush()

    testdb.session.add_all(
        [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
    testdb.session.flush()

    helen_courses = [2, 4]
    helen = Student(id=1, first_name='Helen', last_name='Turner', group_id=1,
                    courses=[testdb.session.query(Course).get(course_id) for course_id in helen_courses])
    testdb.session.add(helen)
    alan_courses = [2, 3]
    alan = Student(id=2, first_name='Alan', last_name='Turing', group_id=3,
                   courses=[testdb.session.query(Course).get(course_id) for course_id in alan_courses])
    testdb.session.add(alan)
    testdb.session.commit()

    response = client.get("/api/v1/students?format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_students

    response = client.get("/api/v1/students?format=xml")
    assert response.status_code == 200
    assert format_output(response.get_data(as_text=True)) == format_output(xml_students)


def test_studentsoperations_post(client, testdb):
    testdb.session.add_all([Group(id=i, name=name) for i, name in enumerate(group_names[:3], 1)])
    testdb.session.flush()

    testdb.session.add_all(
        [Course(id=i, name=course[0], description=course[1]) for i, course in enumerate(course_names[:4], 1)])
    testdb.session.flush()

    helen_courses = [2, 4]
    helen = Student(id=1, first_name='Helen', last_name='Turner', group_id=1,
                    courses=[testdb.session.query(Course).get(course_id) for course_id in helen_courses])
    testdb.session.add(helen)
    testdb.session.commit()

    response = client.post("/api/v1/students?first_name=Alan&last_name=Turing&group_id=3&courses_ids=2%2C3&format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_students_post_ok
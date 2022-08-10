from flask import Flask, request, make_response
from flask_restful import Resource, Api, abort
from sqlalchemy import func

from dicttoxml import dicttoxml
import json

from flasgger import Swagger

from university_accounting import app, db, Group, association_table, Student, Course, courses_dict

api = Api(app)
swagger = Swagger(app)


@api.representation('application/xml')
def output_xml(data, code, headers=None):
    resp = make_response(dicttoxml({'response': data}, attr_type=False), code)
    resp.headers.extend(headers or {})
    return resp


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps({'response': data}, indent=4, sort_keys=False), code)
    resp.headers.extend(headers or {})
    return resp


class GroupsByCount(Resource):

    def get(self):
        """
        Display groups with less or equals student count.
        ----
        tags:
        - groups
        parameters:
        - name: "count"
          in: "query"
          description: "Count of students"
          required: true
          type: "integer"
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "successful operation"
          "400":
            description: "Invalid status value"
        """
        count = request.args.get('count')
        fmt = request.args.get('format')
        groups_counted = db.session.query(Group.id, Group.name, func.count(Student.group_id).label('n_students')) \
            .join(Student).group_by(Group.id).having(func.count(Student.group_id) <= count).all()
        result_dict = {f"group_{group[0]}":
                           {'group_id': str(group[0]),
                            'group_name': group[1],
                            'n_students': str(group[2])}
                       for group in groups_counted}
        if fmt == 'xml':
            return output_xml(result_dict, 200, headers={'Content-Type': 'text/xml'})
        elif fmt == 'json':
            return output_json(result_dict, 200, headers={'Content-Type': 'application/json'})
        else:
            return abort(400, message='Bad Request')


class StudentsOnCourse(Resource):
    def get(self, coursename):
        """
        Display all students related to the course with a given name.
        ----
        tags:
        - courses
        parameters:
        - name: "coursename"
          in: "path"
          description: "Name of the course"
          required: true
          type: "string"
          enum:
            - "discrete_math"
            - "physics"
            - "math_analysis"
            - "english"
            - "programming"
            - "symmetric_cryptography"
            - "asymmetric_cryptography"
            - "combinatorial_analysis"
            - "algorithms"
            - "statistics"
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "successful operation"
          "400":
            description: "Invalid status value"
        """
        course_full_name = courses_dict[coursename]
        fmt = request.args.get('format')
        students_lst = db.session.query(Student.id, Student.first_name, Student.last_name).join(association_table) \
            .join(Course) \
            .filter(Course.name == course_full_name).all()
        result_dict = {f"student_{student[0]}":
                           {'student_id': str(student[0]),
                            'first_name': student[1],
                            'last_name': str(student[2])}
                       for student in students_lst}
        if fmt == 'xml':
            return output_xml(result_dict, 200, headers={'Content-Type': 'text/xml'})
        elif fmt == 'json':
            return output_json(result_dict, 200, headers={'Content-Type': 'application/json'})
        else:
            return abort(400, message='Bad Request')

    def post(self, coursename):
        """
        Add a student to the course with a given name.
        ----
        tags:
        - courses
        parameters:
        - name: "student_id"
          in: "query"
          description: "ID of student to add"
          required: true
          type: "integer"
        - name: "coursename"
          in: "path"
          description: "Name of the course"
          required: true
          type: "string"
          enum:
            - "discrete_math"
            - "physics"
            - "math_analysis"
            - "english"
            - "programming"
            - "symmetric_cryptography"
            - "asymmetric_cryptography"
            - "combinatorial_analysis"
            - "algorithms"
            - "statistics"
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "successful operation"
          "400":
            description: "Invalid status value"
        """
        student_id = request.args.get('student_id')
        fmt = request.args.get('format')
        course_id = list(courses_dict.keys()).index(coursename) + 1
        try:
            the_course = Course.query.get(course_id)
            the_student = Student.query.get(student_id)
            if the_student in the_course.students:
                result_dict = {"code": 400,
                               "message": f"Student with id={student_id} is already "
                                          f"in {list(courses_dict.values())[course_id - 1]} course!"}
            else:
                the_course.students.append(the_student)
                db.session.commit()
                result_dict = {"code": 200,
                               "message":
                                   f"Student with id={student_id} added "
                                   f"to {list(courses_dict.values())[course_id - 1]} course!"}
            if fmt == 'xml':
                return output_xml(result_dict, result_dict['code'], headers={'Content-Type': 'text/xml'})
            elif fmt == 'json':
                return output_json(result_dict, result_dict['code'], headers={'Content-Type': 'application/json'})
        except:
            db.session.rollback()
            return abort(500, message="DB commit failed")

    def delete(self, coursename):
        """
        Remove a student from the course with a given name.
        ----
        tags:
        - courses
        parameters:
        - name: "student_id"
          in: "query"
          description: "ID of student to add"
          required: true
          type: "integer"
        - name: "coursename"
          in: "path"
          description: "Name of the course"
          required: true
          type: "string"
          enum:
            - "discrete_math"
            - "physics"
            - "math_analysis"
            - "english"
            - "programming"
            - "symmetric_cryptography"
            - "asymmetric_cryptography"
            - "combinatorial_analysis"
            - "algorithms"
            - "statistics"
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "successful operation"
          "400":
            description: "Invalid status value"
        """
        student_id = request.args.get('student_id')
        fmt = request.args.get('format')
        course_id = list(courses_dict.keys()).index(coursename) + 1
        try:
            the_course = Course.query.get(course_id)
            the_student = Student.query.get(student_id)
            if the_student not in the_course.students:
                result_dict = {"code": 400,
                               "message": f"Student with id={student_id} is not "
                                          f"in {list(courses_dict.values())[course_id - 1]} course!"}
            else:
                the_course.students.remove(the_student)
                db.session.commit()
                result_dict = {"code": 200,
                               "message":
                                   f"Student with id={student_id} removed "
                                   f"from {list(courses_dict.values())[course_id - 1]} course!"}
            if fmt == 'xml':
                return output_xml(result_dict, result_dict['code'], headers={'Content-Type': 'text/xml'})
            elif fmt == 'json':
                return output_json(result_dict, result_dict['code'], headers={'Content-Type': 'application/json'})
        except:
            db.session.rollback()
            return abort(500, message="DB commit failed")


class StudentsOperations(Resource):
    def get(self):
        """
        Display all students.
        ----
        tags:
        - students
        parameters:
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "successful operation"
          "400":
            description: "Invalid status value"
        """
        fmt = request.args.get('format')
        the_students = Student.query.all()
        result_dict = {f"student_{student.id}":
                           {'student_id': str(student.id),
                            'group_id': str(student.group_id),
                            'first_name': student.first_name,
                            'last_name': student.last_name}
                       for student in the_students}
        if fmt == 'xml':
            return output_xml(result_dict, 200, headers={'Content-Type': 'text/xml'})
        elif fmt == 'json':
            return output_json(result_dict, 200, headers={'Content-Type': 'application/json'})
        else:
            return abort(400, message='Bad Request')

    def post(self):
        """
        Add a new student.
        ----
        tags:
        - students
        parameters:
        - name: "first_name"
          in: "query"
          description: "First name of a student to add"
          required: true
          type: "string"
        - name: "last_name"
          in: "query"
          description: "Last name of a student to add"
          required: true
          type: "string"
        - name: "group_id"
          in: "query"
          description: "ID of a group the student will be added to"
          required: true
          type: "integer"
        - name: "courses_ids"
          in: "query"
          description: "A comma-separated list of courses IDs (numbers 1-10)"
          required: true
          schema:
            type: array
            items:
              type: integer
            minItems: 1
          style: simple
          explode: true
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "Successful operation"
          "400":
            description: "Bad Request"
          "500":
            description: "Internal server error"
        """
        fmt = request.args.get('format')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        group_id = request.args.get('group_id')
        courses_ids = [int(id) for id in request.args.get('courses_ids').split(',')]
        try:
            max_id = db.session.query(func.max(Student.id)).scalar()
            new_student = Student(id=max_id + 1, first_name=first_name, last_name=last_name, group_id=group_id,
                                  courses=[Course.query.get(course_id) for course_id in courses_ids])
            db.session.add(new_student)
            db.session.commit()
            result_dict = {'code': 200,
                           'message': "New student added successfully!",
                           'student_id': str(max_id + 1),
                           'courses_ids': str(courses_ids),
                           'group_id': str(group_id),
                           'first_name': first_name,
                           'last_name': last_name}
            if fmt == 'xml':
                return output_xml(result_dict, result_dict['code'], headers={'Content-Type': 'text/xml'})
            elif fmt == 'json':
                return output_json(result_dict, result_dict['code'], headers={'Content-Type': 'application/json'})
        except:
            db.session.rollback()
            return abort(500, message="DB commit failed")

    def delete(self):
        """
        Remove a student from the course with a given name.
        ----
        tags:
        - students
        parameters:
        - name: "student_id"
          in: "query"
          description: "ID of student to add"
          required: true
          type: "integer"
        - name: "format"
          in: "query"
          description: "Format of response"
          required: true
          type: "string"
          enum:
            - "json"
            - "xml"
        responses:
          "200":
            description: "successful operation"
          "400":
            description: "Invalid status value"
        """
        the_id = request.args.get('student_id')
        fmt = request.args.get('format')
        try:
            the_student = Student.query.get(the_id)
            if the_student:
                student_courses = the_student.courses
                for course in student_courses:
                    course.students.remove(the_student)
                db.session.delete(the_student)
                db.session.commit()
                result_dict = {"code": 200,
                               "message": f"Student with id={the_id} deleted successfully!"}
            else:
                result_dict = {"code": 400,
                               "message": f"Student with id={the_id} is not in the db!"}
            if fmt == 'xml':
                return output_xml(result_dict, result_dict['code'], headers={'Content-Type': 'text/xml'})
            elif fmt == 'json':
                return output_json(result_dict, result_dict['code'], headers={'Content-Type': 'application/json'})
        except:
            db.session.rollback()
            return abort(500, message="DB commit failed")



api.add_resource(GroupsByCount, '/api/v1/groups/by_count')
api.add_resource(StudentsOnCourse, '/api/v1/courses/<coursename>/students')
api.add_resource(StudentsOperations, '/api/v1/students/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

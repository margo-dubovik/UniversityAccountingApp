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
                                   f"to {list(courses_dict.values())[course_id - 1]} course!"}
            if fmt == 'xml':
                return output_xml(result_dict, result_dict['code'], headers={'Content-Type': 'text/xml'})
            elif fmt == 'json':
                return output_json(result_dict, result_dict['code'], headers={'Content-Type': 'application/json'})
        except:
            db.session.rollback()
            return abort(500, message="DB commit failed")


api.add_resource(GroupsByCount, '/api/v1/groups/by_count')
api.add_resource(StudentsOnCourse, '/api/v1/courses/<coursename>/students')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

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
        Function to display groups with less or equals student count.
        ----
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




api.add_resource(GroupsByCount, '/api/v1/groups/by_count')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

import json
from tests.api.varscompare import *


def format_output(text):
    return ''.join(text.split())


def test_groupsbycount(client):
    response = client.get("/api/v1/groups/by_count?count=3&format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_groupsbycount

    response = client.get("/api/v1/groups/by_count?count=3&format=xml")
    assert response.status_code == 200
    assert format_output(response.get_data(as_text=True)) == format_output(xml_groupsbycount)


def test_studentsoncourse_get(client):
    response = client.get("/api/v1/courses/physics/students?format=json")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_studentsoncourse

    response = client.get("/api/v1/courses/physics/students?format=xml")
    assert response.status_code == 200
    assert format_output(response.get_data(as_text=True)) == format_output(xml_studentsoncourse)


def test_studentsoncourse_post(client):
    response = client.post("/api/v1/courses/physics/students?student_id=9&format=xml")
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_studentsoncourse

    response = client.get("/api/v1/courses/physics/students?format=json") # checking if student really is on course
    assert response.status_code == 200
    assert json.loads(response.get_data()) == json_studentsoncourse_updated

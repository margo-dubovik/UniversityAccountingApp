json_groupsbycount = {
    "response": {
        "group_2": {
            "group_id": "2",
            "group_name": "FB-61",
            "n_students": "3"
        },
        "group_3": {
            "group_id": "3",
            "group_name": "SA-72",
            "n_students": "2"
        }
    }
}

xml_groupsbycount = """<?xml version="1.0" encoding="UTF-8" ?>
  <root>
    <response>
      <group_2>
        <group_id>2</group_id>
        <group_name>FB-61</group_name>
        <n_students>3</n_students>
      </group_2>
      <group_3>
        <group_id>3</group_id>
        <group_name>SA-72</group_name>
        <n_students>2</n_students>
      </group_3>
    </response>
  </root>"""

json_studentsoncourse = {
    "response": {
        "student_2": {
            "student_id": "2",
            "first_name": "Helen",
            "last_name": "Turner"
        },
        "student_5": {
            "student_id": "5",
            "first_name": "Andrew",
            "last_name": "Turner"
        },
        "student_8": {
            "student_id": "8",
            "first_name": "Alan",
            "last_name": "Turing"
        }
    }
}

xml_studentsoncourse = """<?xml version="1.0" encoding="UTF-8" ?>
  <root>
    <response>
      <student_2>
        <student_id>2</student_id>
        <first_name>Helen</first_name>
        <last_name>Turner</last_name>
      </student_2>
      <student_5>
        <student_id>5</student_id>
        <first_name>Andrew</first_name>
        <last_name>Turner</last_name>
      </student_5>
      <student_8>
        <student_id>8</student_id>
        <first_name>Alan</first_name>
        <last_name>Turing</last_name>
      </student_8>
    </response>
  </root>"""

json_studentsoncourse_post_ok = {
    "response": {
        "code": 200,
        "message":
            f"Student with id=1 added to Physics course!"}
}

json_studentsoncourse_alreadythere = {
    "response": {
        "code": 400,
        "message": f"Student with id=1 is already in Physics course!"}
}

json_studentsoncourse_delete_ok = {
    "response": {
        "code": 200,
        "message":
            f"Student with id=1 removed from Physics course!"}
}

json_studentsoncourse_notin = {
    "response": {
        "code": 400,
        "message": f"Student with id=1 is not in Physics course!"}
}


# xml_studentsoncourse_post = """<?xml version="1.0" encoding="UTF-8" ?>
#   <root>
#     <response>
#     <code>200</code>
#     <message>Student with id=9 added to Physics course!<message>
#     </response>
#   </root>"""

# json_studentsoncourse_updated = {
#     "response": {
#         "student_2": {
#             "student_id": "2",
#             "first_name": "Helen",
#             "last_name": "Turner"
#         },
#         "student_5": {
#             "student_id": "5",
#             "first_name": "Andrew",
#             "last_name": "Turner"
#         },
#         "student_8": {
#             "student_id": "8",
#             "first_name": "Alan",
#             "last_name": "Turing"
#         },
#         "student_9": {
#             "student_id": "9",
#             "first_name": "Sophia",
#             "last_name": "Roberts"
#         }
#     }
# }

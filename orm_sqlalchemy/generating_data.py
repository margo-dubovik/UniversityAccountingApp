from generator_source import *

import random
import json


def assign_to_groups():
    students = [[random.choice(first_names), random.choice(last_names)] for i in range(200)]
    possible_numbers = list(range(10, 30))
    possible_numbers.append(0)
    students_in_group = random.sample(possible_numbers, 9)
    while 200 - sum(students_in_group) > 30:
        students_in_group = random.sample(range(10, 30), 9)
    students_in_group.append(200 - sum(students_in_group))
    # print(students_in_group)
    random.shuffle(students)
    group_lists = {}
    for i, num in enumerate(students_in_group):
        group_lists[group_names[i]] = (students[:num])
        students = students[num:]

    return group_lists


if __name__ == '__main__':
    groups_dict = assign_to_groups()
    # print(json.dumps(group_lists, indent=1))
    # for groupname in groups_dict.keys():
    #     print(groupname+":")
    #     print(groups_dict[groupname])
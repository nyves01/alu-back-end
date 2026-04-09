#!/usr/bin/python3
"""Gather TODO list progress for a specific employee from a REST API."""

import requests
import sys


if __name__ == "__main__":
    employee_id = int(sys.argv[1])

    base = "https://jsonplaceholder.typicode.com"
    user = requests.get("{}/users/{}".format(base, employee_id)).json()
    todos = requests.get("{}/todos".format(base),
                         params={"userId": employee_id}).json()

    name = user.get("name")
    done = [t for t in todos if t.get("completed")]

    print("Employee {} is done with tasks({}/{}):".format(
        name, len(done), len(todos)))

    for task in done:
        print("\t {}".format(task.get("title")))

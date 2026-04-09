#!/usr/bin/python3
"""Gather TODO list progress for a specific employee from a REST API."""

import requests
import sys


if __name__ == "__main__":
    employee_id = int(sys.argv[1])

    base = "https://jsonplaceholder.typicode.com"

    all_users = requests.get("{}/users".format(base)).json()
    all_todos = requests.get("{}/todos".format(base)).json()

    name = None
    for user in all_users:
        if user["id"] == employee_id:
            name = user["name"]

    todos = [t for t in all_todos if t["userId"] == employee_id]
    done = [t for t in todos if t["completed"]]

    print("Employee {} is done with tasks({}/{}):".format(
        name, len(done), len(todos)))

    for task in done:
        print("\t {}".format(task["title"]))

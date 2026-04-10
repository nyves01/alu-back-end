#!/usr/bin/python3
"""Export a specific employee's TODO list to JSON format."""

import json
import sys
import urllib.parse
import urllib.request


BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_json(url):
    """Fetch and decode JSON payload from a URL."""
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def get_user(user_id):
    """Return user data for a given user id."""
    return fetch_json("{}/users/{}".format(BASE_URL, user_id))


def get_user_todos(user_id):
    """Return TODO items for a given user id."""
    query = urllib.parse.urlencode({"userId": user_id})
    return fetch_json("{}/todos?{}".format(BASE_URL, query))


def main():
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print("employee_id must be an integer", file=sys.stderr)
        sys.exit(1)

    user = get_user(user_id)
    todos = get_user_todos(user_id)

    username = user.get("username")
    file_name = "{}.json".format(user_id)

    user_tasks = []
    for task in todos:
        user_tasks.append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        })

    payload = {str(user_id): user_tasks}

    with open(file_name, "w") as json_file:
        json.dump(payload, json_file)


if __name__ == "__main__":
    main()

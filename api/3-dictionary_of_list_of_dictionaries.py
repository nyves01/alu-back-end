#!/usr/bin/python3
"""Export all employees' TODO lists to a single JSON file."""

import json
import urllib.request


BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_json(url):
    """Fetch and decode JSON payload from a URL."""
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def main():
    """Program entry point."""
    users = fetch_json("{}/users".format(BASE_URL))
    todos = fetch_json("{}/todos".format(BASE_URL))

    usernames_by_id = {}
    for user in users:
        usernames_by_id[user.get("id")] = user.get("username")

    all_tasks = {}
    for task in todos:
        user_id = task.get("userId")
        user_key = str(user_id)
        entry = {
            "username": usernames_by_id.get(user_id),
            "task": task.get("title"),
            "completed": task.get("completed")
        }
        all_tasks.setdefault(user_key, []).append(entry)

    with open("todo_all_employees.json", "w") as json_file:
        json.dump(all_tasks, json_file)


if __name__ == "__main__":
    main()

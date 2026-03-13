from demo_project.app.task_model import Task


def get_todos():
    tasks = None  # BUG: should be an empty list
    return [task.to_dict() for task in tasks]


def count_todos():
    return len(get_todos())
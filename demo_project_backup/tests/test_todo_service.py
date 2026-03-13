from app.todo_service import get_todos, count_todos


def test_get_todos_returns_list():
    result = get_todos()
    assert isinstance(result, list)


def test_get_todos_default_empty():
    result = get_todos()
    assert result == []


def test_count_todos_default_zero():
    assert count_todos() == 0

# TODO(student):
# Add test cases for the new feature:
# count_completed_tasks(tasks)
#
# Suggested cases:
# 1. empty task list
# 2. all tasks incomplete
# 3. some tasks completed
# 4. all tasks completed
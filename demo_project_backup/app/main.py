from demo_project.app.todo_service import get_todos


def main():
    todos = get_todos()
    for todo in todos:
        print(todo)


if __name__ == "__main__":
    main()
class Task:
    def __init__(self, title: str, completed: bool = False):
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed
        }
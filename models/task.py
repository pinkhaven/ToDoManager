class Task:
    def __init__(self, title, description, due_date, priority, is_done=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.is_done = is_done
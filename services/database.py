import sqlite3
from models import event
from models import task


class DatabaseService:
    @staticmethod
    def setup_database():
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (title TEXT, description TEXT, due_date TEXT, priority TEXT, is_done INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS events
                     (title TEXT, description TEXT, event_date TEXT)''')
        conn.commit()
        conn.close()

    @staticmethod
    def add_task(task):
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks VALUES (?,?,?,?,?)",
                  (task.title, task.description, task.due_date, task.priority, task.is_done))
        conn.commit()
        conn.close()

    @staticmethod
    def get_tasks():
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
        conn.close()
        return tasks

    @staticmethod
    def update_task(task):
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks 
                           SET description=?, due_date=?, priority=?, is_done=? 
                           WHERE title=?''',
                  (task.description, task.due_date, task.priority, task.is_done, task.title))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_task(task_title):
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE title=?", (task_title,))
        conn.commit()
        conn.close()

    @staticmethod
    def add_event(event):
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute("INSERT INTO events VALUES (?,?,?)",
                  (event.title, event.description, event.event_date))
        conn.commit()
        conn.close()

    @staticmethod
    def get_events():
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute("SELECT * FROM events")
        events = c.fetchall()
        conn.close()
        return events


    @staticmethod
    def delete_event(event_title):
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute("DELETE FROM events WHERE title=?", (event_title,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_event(event):
        conn = sqlite3.connect('todomanager.db')
        c = conn.cursor()
        c.execute('''UPDATE events 
                     SET description=?, event_date=? 
                     WHERE title=?''',
                  (event.description, event.event_date, event.title))
        conn.commit()
        conn.close()

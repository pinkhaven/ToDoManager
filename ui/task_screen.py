from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from services.database import DatabaseService
from models.task import Task

class TaskScreen(Screen):
    def __init__(self, **kwargs):
        super(TaskScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add input fields
        self.title_input = TextInput(hint_text='Title')
        self.description_input = TextInput(hint_text='Description')
        self.due_date_input = TextInput(hint_text='Due Date')
        self.priority_input = TextInput(hint_text='Priority')
        self.is_done_input = TextInput(hint_text='Is Done (0 or 1)')

        layout.add_widget(self.title_input)
        layout.add_widget(self.description_input)
        layout.add_widget(self.due_date_input)
        layout.add_widget(self.priority_input)
        layout.add_widget(self.is_done_input)

        # Add buttons
        save_button = Button(text='Save Task', on_release=self.save_task)
        layout.add_widget(save_button)

        delete_button = Button(text='Delete Task', on_release=self.delete_task)
        layout.add_widget(delete_button)

        back_button = Button(text='Back', on_release=self.goto_main_screen)
        layout.add_widget(back_button)

        # Add scroll view for displaying tasks
        scroll_view = ScrollView()
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))

        self.load_tasks()

        scroll_view.add_widget(self.tasks_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def save_task(self, instance):
        task = Task(self.title_input.text,
                    self.description_input.text,
                    self.due_date_input.text,
                    self.priority_input.text,
                    int(self.is_done_input.text))
        DatabaseService.add_task(task)
        self.clear_inputs()
        self.load_tasks()

    def delete_task(self, instance):
        task_title = self.title_input.text
        DatabaseService.delete_task(task_title)
        self.clear_inputs()
        self.load_tasks()

    def load_tasks(self):
        self.tasks_layout.clear_widgets()
        tasks = DatabaseService.get_tasks()
        for task_data in tasks:
            task = Task(*task_data)
            task_label = Label(text=f'Title: {task.title}\nDescription: {task.description}\n'
                                   f'Due Date: {task.due_date}\nPriority: {task.priority}\n'
                                   f'Is Done: {"Yes" if task.is_done else "No"}',
                               size_hint_y=None, height=100)
            self.tasks_layout.add_widget(task_label)

    def clear_inputs(self):
        self.title_input.text = ''
        self.description_input.text = ''
        self.due_date_input.text = ''
        self.priority_input.text = ''
        self.is_done_input.text = ''

    def goto_main_screen(self, instance):
        self.manager.current = 'main'


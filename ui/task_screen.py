from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from services.database import DatabaseService
from services.camera import CameraService
from models.task import Task
from services.gps import GPSService


class TaskScreen(Screen):
    def __init__(self, **kwargs):
        super(TaskScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.camera_service = CameraService()
        self.gps_service = GPSService()

        # Add input fields
        self.title_input = TextInput(hint_text='Title', size_hint=(0.8, None), height=50)
        self.description_input = TextInput(hint_text='Description', size_hint_y=0.1)
        self.due_date_input = TextInput(hint_text='Due Date', size_hint_y=0.1)
        self.priority_input = TextInput(hint_text='Priority', size_hint_y=0.1)
        self.is_done_input = TextInput(hint_text='Is Done (0 or 1)', size_hint_y=0.1)
        self.gps_input = TextInput(hint_text='Current location', disabled=True)

        self.back_button = Button(text='Back', size_hint=(0.2, None), height=50, on_release=self.goto_main_screen)
        self.gps_button = Button(text='GPS', size_hint=(0.2, None), height=50)

        title_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'x': 0, 'y': 1})
        title_layout.add_widget(self.title_input)
        title_layout.add_widget(self.back_button)

        gps_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        gps_layout.add_widget(self.gps_input)
        gps_layout.add_widget(self.gps_button)

        # Layout
        layout.add_widget(title_layout)

        layout.add_widget(self.description_input)
        layout.add_widget(self.due_date_input)
        layout.add_widget(self.priority_input)
        layout.add_widget(self.is_done_input)

        layout.add_widget(gps_layout)

        # Add buttons in a horizontal BoxLayout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'x': 0, 'y': 0})
        save_button = Button(text='Save Task', on_release=self.save_task)
        edit_button = Button(text='Edit Task', on_release=self.edit_task)
        delete_button = Button(text='Delete Task', on_release=self.delete_task)
        picture_button = Button(text='Add Picture', on_release=self.use_camera)

        button_layout.add_widget(save_button)
        button_layout.add_widget(edit_button)
        button_layout.add_widget(delete_button)
        button_layout.add_widget(picture_button)

        # Add scroll view for displaying tasks
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))

        self.load_tasks()

        scroll_view.add_widget(self.tasks_layout)
        layout.add_widget(scroll_view)

        # Add the button layout to the bottom of the screen
        relative_layout = RelativeLayout()
        relative_layout.add_widget(layout)
        relative_layout.add_widget(button_layout)
        self.add_widget(relative_layout)

    def save_task(self, instance):
        task = Task(self.title_input.text,
                    self.description_input.text,
                    self.due_date_input.text,
                    self.priority_input.text,
                    int(self.is_done_input.text))
        DatabaseService.add_task(task)
        self.clear_inputs()
        self.load_tasks()

    def edit_task(self, instance):
        task = Task(self.title_input.text,
                    self.description_input.text,
                    self.due_date_input.text,
                    self.priority_input.text,
                    int(self.is_done_input.text))
        DatabaseService.update_task(task)
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
            task_button = Button(text=f'Title: {task.title}\nDescription: {task.description}\n'
                                      f'Due Date: {task.due_date}\nPriority: {task.priority}\n'
                                      f'Is Done: {"Yes" if task.is_done else "No"}',
                                 size_hint_y=None, height=100, on_release=self.load_task_data)
            task_button.task_data = task_data
            self.tasks_layout.add_widget(task_button)

    def load_task_data(self, instance):
        task_data = instance.task_data
        self.title_input.text = task_data[0]
        self.description_input.text = task_data[1]
        self.due_date_input.text = task_data[2]
        self.priority_input.text = task_data[3]
        self.is_done_input.text = str(task_data[4])

    def clear_inputs(self):
        self.title_input.text = ''
        self.description_input.text = ''
        self.due_date_input.text = ''
        self.priority_input.text = ''
        self.is_done_input.text = ''

    def goto_main_screen(self, instance):
        self.manager.current = 'main'

    def use_camera(self, instance):
        self.camera_service.show_camera()


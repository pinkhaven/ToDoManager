from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from resources.strings import APP_NAME
from ui.main_screen import MainScreen
from ui.task_screen import TaskScreen
from ui.event_screen import EventScreen
from services.database import DatabaseService

class ToDoManagerApp(App):
    def build(self):
        self.title = APP_NAME
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TaskScreen(name='task'))
        sm.add_widget(EventScreen(name='event'))
        return sm


if __name__ == '__main__':
    DatabaseService.setup_database()

    Window.size = (360, 640)

    ToDoManagerApp().run()

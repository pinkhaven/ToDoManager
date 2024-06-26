from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from services.camera import CameraService


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        layout = BoxLayout(orientation='vertical')

        task_button = Button(text='Tasks', on_release=self.goto_task_screen)
        event_button = Button(text='Events', on_release=self.goto_event_screen)

        layout.add_widget(task_button)
        layout.add_widget(event_button)

        anchor_layout.add_widget(layout)
        self.add_widget(anchor_layout)

    def goto_task_screen(self, instance):
        self.manager.current = 'task'

    def goto_event_screen(self, instance):
        self.manager.current = 'event'

    def show_location(self, instance):
        lat, lon = self.gps_service.get_location()
        popup = Popup(title='Location', content=Label(text=f"Latitude: {lat}, Longitude: {lon}"), size_hint=(0.8, 0.8))
        popup.open()

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from services.camera import CameraService
from services.gps import GPSService


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        task_button = Button(text='Tasks', on_release=self.goto_task_screen)
        event_button = Button(text='Events', on_release=self.goto_event_screen)
        camera_button = Button(text='Camera', on_release=self.use_camera)
        gps_button = Button(text='GPS', on_release=self.show_location)

        layout.add_widget(task_button)
        layout.add_widget(event_button)
        layout.add_widget(camera_button)
        layout.add_widget(gps_button)
        self.add_widget(layout)

        self.camera_service = CameraService()
        self.gps_service = GPSService()

    def goto_task_screen(self, instance):
        self.manager.current = 'task'

    def goto_event_screen(self, instance):
        self.manager.current = 'event'

    def use_camera(self, instance):
        self.camera_service.show_camera()

    def show_location(self, instance):
        lat, lon = self.gps_service.get_location()
        popup = Popup(title='Location', content=Label(text=f"Latitude: {lat}, Longitude: {lon}"), size_hint=(0.8, 0.8))
        popup.open()

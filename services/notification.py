from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class NotificationService:
    @staticmethod
    def notify(message):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=message))
        btn = Button(text='OK')
        layout.add_widget(btn)
        popup = Popup(title='Notification', content=layout, size_hint=(0.5, 0.5))
        btn.bind(on_press=popup.dismiss)
        popup.open()

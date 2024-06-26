import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class CameraService:
    def __init__(self):
        self.capture = None
        self.image_widget = Image()
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.image_widget)
        capture_button = Button(text="Capture", size_hint=(1, 0.2))
        capture_button.bind(on_press=self.take_picture)
        self.layout.add_widget(capture_button)

    def show_camera(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        popup = Popup(title="Camera", content=self.layout, size_hint=(0.8, 0.8))
        popup.open()

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image_widget.texture = texture

    def take_picture(self, instance):
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite('picture.png', frame)
            print("Picture taken and saved as picture.png")

        if self.capture:
            self.capture.release()
        Clock.unschedule(self.update)


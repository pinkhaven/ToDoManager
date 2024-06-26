from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from services.database import DatabaseService
from models.event import Event


class EventScreen(Screen):
    def __init__(self, **kwargs):
        super(EventScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add input fields
        self.title_input = TextInput(hint_text='Title', size_hint_y=0.1)
        self.description_input = TextInput(hint_text='Description', size_hint_y=0.1)
        self.event_date_input = TextInput(hint_text='Event Date', size_hint_y=0.1)

        layout.add_widget(self.title_input)
        layout.add_widget(self.description_input)
        layout.add_widget(self.event_date_input)

        # Add buttons in horizontal BoxLyout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'x': 0, 'y': 0})
        save_button = Button(text='Save Event', on_release=self.save_event)
        edit_button = Button(text='Edit Event', on_release=self.edit_event)
        delete_button = Button(text='Delete Event', on_release=self.delete_event)
        back_button = Button(text='Back', on_release=self.goto_main_screen)
        button_layout.add_widget(save_button)
        button_layout.add_widget(edit_button)
        button_layout.add_widget(delete_button)
        button_layout.add_widget(back_button)

        # Add scroll view for displaying events
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.events_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.events_layout.bind(minimum_height=self.events_layout.setter('height'))

        self.load_events()

        scroll_view.add_widget(self.events_layout)
        layout.add_widget(scroll_view)

        # Add the button layout to the bottom of the screen
        relative_layout = RelativeLayout()
        relative_layout.add_widget(layout)
        relative_layout.add_widget(button_layout)
        self.add_widget(relative_layout)

    def save_event(self, instance):
        event = Event(self.title_input.text,
                      self.description_input.text,
                      self.event_date_input.text)
        DatabaseService.add_event(event)
        self.clear_inputs()
        self.load_events()

    def edit_event(self, instance):
        event = Event(self.title_input.text,
                      self.description_input.text,
                      self.event_date_input.text)
        DatabaseService.update_event(event)
        self.clear_inputs()
        self.load_events()

    def delete_event(self, instance):
        event_title = self.title_input.text
        DatabaseService.delete_event(event_title)
        self.clear_inputs()
        self.load_events()

    def load_events(self):
        self.events_layout.clear_widgets()
        events = DatabaseService.get_events()
        for event_data in events:
            event = Event(*event_data)
            event_button = Button(text=f'Title: {event.title}\nDescription: {event.description}\n'
                                       f'Event Date: {event.event_date}',
                                  size_hint_y=None, height=100, on_release=self.load_event_data)
            event_button.event_data = event_data
            self.events_layout.add_widget(event_button)

    def load_event_data(self, instance):
        event_data = instance.event_data
        self.title_input.text = event_data[0]
        self.description_input.text = event_data[1]
        self.event_date_input.text = event_data[2]

    def clear_inputs(self):
        self.title_input.text = ''
        self.description_input.text = ''
        self.event_date_input.text = ''

    def goto_main_screen(self, instance):
        self.manager.current = 'main'

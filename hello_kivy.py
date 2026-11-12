from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class HelloKivyApp(App):

    def build(self):

        # Create layout
        layout = BoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20
        )

        # Create label
        label = Label(text="Welcome to Kivy!")

        # Create button
        button = Button(text="Click Me")
        button.bind(on_press=self.show_message)

        # Add widgets to layout
        layout.add_widget(label)
        layout.add_widget(button)

        return layout

    def show_message(self, instance):

        popup = Popup(
            title="Message",
            content=Label(text="Hello! You clicked the button."),
            size_hint=(0.7, 0.4)
        )

        popup.open()


# Run application
HelloKivyApp().run()
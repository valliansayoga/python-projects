"""
Aplikasi motivator yang akan membuat hari-hari pengguna lebih berwarna.

Use with caution!
"""
from kivy.app import App
from kivy.lang import Builder  # To connect with the KV file
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
import random


Builder.load_file("design.kv")


class LoginScreen(Screen):  # Empty class to refer the same name in KV file
    def sign_up(self):
        self.manager.transition_direction = "left"
        self.manager.current = "sign_up_screen"

    def log_in(self, uname, pword):
        with open("users.json") as js:
            users = json.load(js)
        if uname in users and users[uname]["password"] == pword:
            self.manager.transition.direction = "down"
            self.manager.current = "login_success_screen"
            self.ids.login_wrong.text = ""
        else:
            self.ids.login_wrong.text = "Wrong username or password!"

    def forgot_pass_screen(self):
        self.manager.transition_direction = "down"
        self.manager.current = "forgot_password_screen"


class RootWidget(ScreenManager):  # Every part in KV must have an empty class
    pass


class MainApp(App):
    def build(self):
        return RootWidget()  # Initializing the RootWidget obj, not class


class SignUpScreen(Screen):  # Deklarasi class
    def add_user(self, uname, pword):
        with open("users.json") as js:
            users = json.load(js)
        users[uname] = {
            "username": uname,
            "password": pword,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open("users.json", "w") as js:  # To overwrite the JSON
            json.dump(users, js)
        self.manager.current = "sign_up_success_screen"

    def go_to_login2(self):
        self.manager.current = "login_screen"
        self.manager.transition.direction = "right"


class SignUpSuccessScreen(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"  # Transition
        self.manager.current = "login_screen"


class LoginSuccessScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = "up"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open(
                f"quotes/{feel}.txt", encoding="utf8"
            ) as file:  # To set the encoding. It caused an error if not used
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = (
                "Sorry, currently I don't know what to tell you based on that feeling."
            )


class ImageButton(
    ButtonBehavior, HoverBehavior, Image
):  # ButtonBehavior harus duluan supaya bisa diklik
    pass


class ForgotPasswordScreen(Screen):
    def forgot_pass(self, uname):
        with open("users.json") as js:
            users = json.load(js)
            self.ids.password.text = f"Your password is: {users[uname]['password']}"

    def go_to_login(self):
        self.manager.transition.direction = "up"  # Transition
        self.manager.current = "login_screen"


if __name__ == "__main__":
    MainApp().run()

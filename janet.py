from modules import library, triggers
from modules.speech import Speech
from frontend.models import UserUtils
from syntax.syntax import greetings

from dotenv import load_dotenv, find_dotenv
import random

load_dotenv(find_dotenv())


class Janet:
    def __init__(self, app_library):
        self.app_lib = app_library

        self.speech = Speech()
        self.user_utils = UserUtils(self.speech)

        self.user = self.user_utils.get_current_user()
        if not self.user:
            self.user = self.user_utils.login_or_create_user()
        self.username = self.user.username if self.user else None

    def goodbye(self):
        self.speech.speak("Goodbye!")
        exit()

    def entry(self):
        self.speech.speak(
            f"{greetings[random.randint(0, len(greetings) - 1)]} {self.username}"
        )

        JANET = True
        while JANET:
            print("Awaiting your command!!")

            response = None
            # self.triggers = triggers
            # self.triggers.run()

            janet_command = self.speech.listen()
            if " ".join(janet_command).lower() == "goodbye janet":
                self.goodbye()

            app = self.app_lib.select(janet_command)
            if app:
                _cls = app.get_class()
                _class = _cls(self.speech)

                # TODO: Sort out the thread Q - thread pool?
                if app.janet_input:
                    app.kwargs["janet_command"] = janet_command

                method = getattr(_class, app.method)
                response = method(*app.args, **app.kwargs)

            if response:
                self.speech.speak(response)


def run():
    app_library = library.AppController()

    janet = Janet(app_library)
    try:
        janet.entry()
    except KeyboardInterrupt:
        janet.goodbye()


if __name__ == "__main__":
    run()

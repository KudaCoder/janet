from modules.storage.database import Database
from modules.comm.command import MExchange
from modules.speech import Speech
from modules import library, triggers

from syntax.syntax import greetings

import threading
import random


class Janet:
    def __init__(self, app_library, message_server=None, db_controller=None):
        self.db_controller = db_controller
        self.db = None
        self.user = None
        if self.db_controller:
            self.db, self.user = self.db_controller.open_session()
        self.username = self.user.username if self.user else None

        self.server = message_server
        self.receive_thread = threading.Thread(target=self.server.receive, daemon=True)
        self.receive_thread.start()

        self.app_lib = app_library
        self.speech = Speech()

    def goodbye(self):
        self.db_controller.close_session()
        self.server.destroy()

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
            self.triggers = triggers
            self.triggers.run()

            janet_command = self.speech.listen()
            if " ".join(janet_command).lower() == "goodbye janet":
                self.goodbye()

            app = self.app_lib.select(janet_command)
            if app:
                _cls = app.get_class()
                _class = _cls(self.speech)

                # TODO: Sort out the thread Q - thread pool?
                if app.janet_input:
                    app.kwargs["janet_command"] = " ".join(janet_command)

                method = getattr(_class, app.method)
                response = method(*app.args, **app.kwargs)

            if response:
                self.speech.speak(response)


if __name__ == "__main__":
    app_library = library.AppController()
    server = MExchange()
    dbc = Database()

    janet = Janet(app_library, db_controller=dbc, message_server=server)
    try:
        janet.entry()
    except KeyboardInterrupt:
        janet.goodbye()

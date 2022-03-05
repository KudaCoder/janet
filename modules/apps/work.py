from frontend.models import WorkUtils, User


class WorkController:
    commands = {
        "work": [
            dict(
                method="start_work",
                keywords=[
                    {
                        "start": {
                            "janet_input": True,
                            "thread_q": False,
                            "args": [],
                            "kwargs": {},
                        }
                    }
                ],
            ),
            dict(
                method="stop_work",
                keywords=[
                    {
                        "stop": {
                            "janet_input": False,
                            "thread_q": False,
                            "args": [],
                            "kwargs": {},
                        }
                    }
                ],
            ),
        ],
        "job": [
            dict(
                method="start_task",
                keywords=[
                    {
                        "start": {
                            "janet_input": False,
                            "thread_q": False,
                            "args": [],
                            "kwargs": {},
                        }
                    }
                ],
            ),
            dict(
                method="stop_task",
                keywords=[
                    {
                        "stop": {
                            "janet_input": False,
                            "thread_q": False,
                            "args": [],
                            "kwargs": {},
                        }
                    }
                ],
            ),
        ],
    }

    def __init__(self, speech):
        self.speech = speech
        self.w_utils = WorkUtils(self.speech)

        self.user = User.current_user()
        self.client, self.project, self.task = self.w_utils.return_active()

    def start_work(self, janet_command=None):
        if self.client:
            self.speech.speak(f"Already working for {self.client.name}")
            return

        if self.speech.filter_response(janet_command, keywords=["for"]):
            client_name = " ".join(janet_command).split("for ")[1]
            self.client = self.w_utils.find_client(name=client_name)
        if not self.client:
            self.client = self.w_utils.which_client()
        if self.client and not self.client.is_active:
            self.w_utils.toggle_active_client(self.client.id)

        return f"The active client is {self.client.name}"

    def stop_work(self):
        if self.client and self.client.is_active:
            self.w_utils.toggle_active_client(self.client.id)
        if self.project and self.project.is_active:
            self.w_utils.toggle_active_project(self.project.id)
        if self.task and self.task.is_active:
            self.stop_task()

        return "Work stopped!"

    def start_task(self):
        if not self.task:
            self.task = self.w_utils.which_task()
        if self.task:
            self.w_utils.start_task(self.task)
            return f"Logging hours for {self.task.title}"

        return "Sorry, there was an issue starting the job!"

    def stop_task(self):
        if not self.task:
            return "No active task!"

        self.w_utils.stop_task(self.task)

        return f"Stopping logging hours for {self.task.title}"

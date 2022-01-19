from modules.utils import WorkUtils

from modules.storage.database import Database
from modules.storage.models import Client

import time


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
                method="start_job",
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
                method="stop_job",
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
        self.db_controller = Database()
        if self.db_controller:
            self.db, self.user = self.db_controller.open_session()
            self.client, self.project, self.job = self.db_controller.return_active()

        self.speech = speech
        self.w_utils = WorkUtils(self.speech)

    def start_work(self, janet_command=None):
        if self.client:
            self.speech.speak(f"Already working for {self.client.name}")
            return

        if self.speech.filter_response(janet_command, keywords=["for"]):
            client_name = janet_command.split("for ")[1]
            self.client = self.db.query(Client).filter_by(name=client_name).first()
        if not self.client:
            self.client = self.w_utils.which_client(self.user, self.db)
        if self.client:
            self.client.is_active = True
            self.client.save(self.db)

        return f"The active client is {self.client.name}"

    def stop_work(self):
        if self.job:
            if self.job.is_active:
                self.stop_job()
        if self.client:
            self.client.is_active = False
            self.client.save(self.db)
        if self.project and self.project.is_active:
            self.project.is_active = False
            self.project.save(self.db)
        if self.job and self.job.is_active:
            self.stop_job()

        return "Work stopped!"

    def start_job(self):
        if not self.job:
            self.job = self.w_utils.which_job(self.user, self.client, self.db)
        if self.job:
            self.job.is_active = True
            self.job.save(self.db)

            self.start_time = time.time()
            return f"Logging hours for {self.job.title}"

        return "Sorry, there was an issue starting the job!"

    def stop_job(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        hours = round(total_time * 2) / 2
        if hours < 0.25:
            hours = 0.5

        self.job.hours = hours
        self.job.is_active = False
        self.job.save(self.db)

        return f"Stopping logging hours for {self.job.title}"

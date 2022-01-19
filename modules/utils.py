from modules.storage.utils import create_new_client, create_new_job, create_new_project
from modules.storage.models import Client, Job, Project

from word2number import w2n


class WorkUtils:
    def __init__(self, speech):
        self.speech = speech

    def which_client(self, user, db):
        response = None
        while True:
            self.speech.speak("Which client are we working for?")
            response = self.speech.listen()
            if self.speech.filter_response(response, keywords=["stop"]):
                return

            if self.speech.filter_response(response, keywords=[""]):
                continue

            client_name = response
            active_client = db.query(Client).filter_by(name=client_name).first()
            if active_client is None:
                self.speech.speak(f"Do you want to add new client {client_name}")
                response = self.speech.listen()
                if self.speech.filter_response(response, keywords=["stop"]):
                    return

                if not self.speech.filter_response(
                    response, keywords=["ye", "yes", "yeah", "add", "new"]
                ):
                    self.speech.speak("Ok")
                    continue

                active_client = create_new_client(client_name, user.id, db)
            if active_client:
                break

        return active_client

    def which_job(self, user, client, db):
        response = None
        job = None
        project = None
        while True:
            self.speech.speak("What job are we working on?")
            response = self.speech.listen()
            if self.speech.filter_response(response, keywords=["stop"]):
                return

            if self.speech.filter_response(response, keywords=[""]):
                self.speech.speak("Sorry, didn't get that!")
                continue

            job_name = response
            job = db.query(Job).filter(Job.title.contains(job_name)).first()
            if not job:
                self.speech.speak(f"Do you want to start new job {job_name}")
                response = self.speech.listen()
                if self.speech.filter_response(response, keywords=["stop"]):
                    return

                if not self.speech.filter_response(
                    response, keywords=["ye", "yes", "yeah", "start", "new"]
                ):
                    self.speech.speak("Ok")
                    continue

                job = create_new_job(job_name, client.id, user.id, db)
            if job:
                break

        if job and not job.project_id:
            while True:
                self.speech.speak("Which project do you want to assign this job too?")
                response = self.speech.listen()
                if self.speech.filter_response(response, keywords=["stop"]):
                    return

                project_name = response
                project = (
                    db.query(Project)
                    .filter(Project.name.contains(project_name))
                    .first()
                )

                if self.speech.filter_response(response, keywords=["new", "project"]):
                    self.speech.speak("What name do you want to give this project?")
                    project_name = self.speech.listen()

                self.speech.speak(
                    f"That's a name of {project_name}. Shall I save this project?"
                )
                response = self.speech.listen()
                if self.speech.filter_response(
                    response, keywords=["ye", "yes", "yeah", "add", "new"]
                ):
                    project = create_new_project(project_name, client.id, db)
                    project.is_active = True
                    project.save(db)
                    break

        if job:
            if project:
                job.project_id = project.id
            job.save(db)
            return job

        return

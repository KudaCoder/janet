from . import db, User, Client, Project, Task

from datetime import datetime


class WorkUtils:
    def __init__(self, speech):
        self.speech = speech

    def return_active(self):
        client = Client.find(is_active=True)
        project = Project.find(is_active=True)
        task = Task.find(is_active=True)
        return client, project, task

    def toggle_active_client(self, client_id):
        client = Client.query.get(client_id)
        if client:
            client.is_active = not client.is_active
        db.session.commit()

    def new_client(self, name=None):
        client_name = None

        if name is not None:
            self.speech.speak(f"Do you want to add new client {name}")
            response = self.speech.listen()
            if self.speech.filter_response(
                response, keywords=["ye", "yes", "yeah", "add", "new"]
            ):
                client_name = name

        if client_name is None:
            self.speech.speak("What name do you want to give this client?")
            response = self.speech.listen()
            client_name = " ".join(response).strip()

        client = Client()
        client.name = client_name
        db.session.add(client)
        db.session.commit()
        return client

    def which_client(self):
        response = None
        while True:
            self.speech.speak("Which client are we working for?")
            response = self.speech.listen()
            if self.speech.filter_response(response, keywords=["stop"]):
                return

            if self.speech.filter_response(response, keywords=[""]):
                continue

            client_name = " ".join(response).strip()
            active_client = Client.find(name=client_name)
            if active_client is None:
                active_client = self.new_client(name=client_name)
            if active_client:
                break

        return active_client

    def toggle_active_project(self, project_id):
        project = Project.query.get(project_id)
        if project:
            project.is_active = not project.is_active
        db.session.commit()

    def new_project(self, name=None):
        project_name = None

        if name is not None:
            self.speech.speak(f"Do you want to create new project {name}")
            response = self.speech.listen()
            if self.speech.filter_response(response, keywords=["stop"]):
                return

            if self.speech.filter_response(
                response, keywords=["ye", "yes", "yeah", "start", "new"]
            ):
                project_name = name

        if project_name is None:
            self.speech.speak("What name do you want to give this project?")
            response = self.speech.listen()
            project_name = " ".join(response).strip()

        user = User.current_user()
        client = Client.find(is_active=True)
        project = Project()
        project.name = project_name
        project.creator_id = user.id
        project.client_id = client.id
        db.session.add(project)
        db.session.commit()
        return project

    def which_project(self):
        self.speech.speak("Which project are we working on?")
        response = self.speech.listen()
        if self.speech.filter_response(response, keywords=["stop"]):
            return

        project_name = " ".join(response).strip()
        project = Project.query.filter_by(name=project_name).first()

        if project is None:
            project = self.new_project(name=project_name)

        return project

    def toggle_active_task(self, task_id):
        task = Task.query.get(task_id)
        if task:
            task.is_active = not task.is_active
        db.session.commit()

    def find_task(self, **kwargs):
        if kwargs.get("title"):
            return Task.query.filter_by(title=kwargs.get("title")).first()

    def new_task(self, task_name=None, project_id=None):
        title = None

        if task_name is not None:
            self.speech.speak(f"Do you want to create new task {task_name}")
            response = self.speech.listen()
            if self.speech.filter_response(response, keywords=["stop"]):
                return

            if self.speech.filter_response(
                response, keywords=["ye", "yes", "yeah", "start", "new"]
            ):
                title = task_name

        if title is None:
            self.speech.speak("What name do you want to give this task?")
            response = self.speech.listen()
            title = " ".join(response).strip()

        user = User.current_user()
        task = Task()
        task.title = title
        task.worker_id = user.id
        if project_id is not None:
            task.project_id = project_id
            db.session.add(task)
            db.session.commit()

        return task

    def which_task(self):
        response = None
        task = None
        project = None

        self.speech.speak("What task are we working on?")
        response = self.speech.listen()
        if self.speech.filter_response(response, keywords=["stop"]):
            return

        task_name = " ".join(response).strip()
        task = self.find_task(title=task_name)
        if not task:
            task = self.new_task(task_name=task_name)

        if task and not task.project_id:
            self.speech.speak("No project ID detected!")
            project = self.which_project()
            task.project_id = project.id

        db.session.add(task)
        db.session.commit()
        return task

    def start_task(self, task):
        task.is_active = True
        task.start_time = datetime.now()
        db.session.commit()

    def stop_task(self, task):
        task.end_time = datetime.now()
        task.is_active = False
        db.session.commit()


class UserUtils:
    def __init__(self, speech):
        self.speech = speech

    def get_current_user(self):
        return User.current_user()

    def login_or_create_user(self):
        users = User.query
        if users.count() == 0:
            user = self.new_user()
        else:
            user = self.login_user()

        return user

    def new_user(self):
        self.speech.speak("What username would you like to give this new user?")
        username = self.speech.listen()
        user = User()
        user.username = " ".join(username).strip()
        user.is_active = True
        self.speech.speak(f"Creating new user {user.username}!")
        db.session.add(user)
        db.session.commit()
        return user

    def login_user(self):
        self.speech.speak("Would you like to login or continue as guest?")
        response = self.speech.listen()
        if self.speech.filter_response(response, keywords=["continue", "guest"]):
            return

        while True:
            self.speech.speak("What username would you like to login with?")
            username = self.speech.listen()
            username = " ".join(username).strip()
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.speech.speak("Sorry, no user with that username exists!")
                continue

            return user

    def delete_user(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

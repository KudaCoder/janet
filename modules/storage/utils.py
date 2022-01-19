from .models import Client, Job, Project


def create_new_client(client_name, user_id, db_session):
    new_client = Client()
    new_client.name = client_name.lower()
    new_client.user_id = user_id
    new_client.save(db_session)

    return new_client


def create_new_job(title, client_id, user_id, db_session):
    new_job = Job()
    new_job.title = title.lower()
    new_job.client_id = client_id
    new_job.user_id = user_id
    new_job.save(db_session)

    return new_job


def create_new_project(name, client_id, db_session):
    new_project = Project()
    new_project.name = name
    new_project.client_id = client_id
    new_project.save(db_session)

    return new_project

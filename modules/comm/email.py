import os
import pickle
from base64 import urlsafe_b64encode

from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


GMAIL_API_ID = os.environ.get("GMAIL_API_ID")
GMAIL_API_SECRET = os.environ.get("GMAIL_API_SECRET")
SCOPES = os.environ.get("SCOPES")
OUR_EMAIL = os.environ.get("OUR_EMAIL")


def get_session_cookies():
    with open("cookies", "rb") as f:
        cookies = pickle.load(f)
    return cookies


def gmail_authenticate():
    creds = None
    if os.path.exists("conf/token.pickle"):
        with open("conf/token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "conf/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("conf/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)


def build_message(sent_to, subject, body):
    message = MIMEText(body)
    message["to"] = sent_to
    message["from"] = OUR_EMAIL
    message["subject"] = subject
    return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}


def send_email(subject, body):
    try:
        service = gmail_authenticate()
        return (
            service.users()
            .messages()
            .send(
                userId="me",
                body=build_message(OUR_EMAIL, subject, body),
            )
            .execute()
        )
    except Exception as e:
        print(e)

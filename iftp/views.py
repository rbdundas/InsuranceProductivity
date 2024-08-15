import os.path
import email
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.shortcuts import render
from InsuranceProductivitiy import settings


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_message(service, msg_id):
    try:
        message_list = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))
        msg_str = email.message_from_bytes(msg_raw)
        content_types = msg_str.get_content_maintype()

        if content_types == 'multipart':
            part1 = msg_str.get_payload()
            return part1.get_payload()
        else:
            return msg_str.get_payload()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def get_new_gmail(request):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{settings.BASE_DIR}/iftp/gmail_iftp_connection.json', SCOPES
            )
            creds = flow.run_local_server(port=8001)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    messages = []
    try:
        service = build("gmail", "v1", credentials=creds)
        result_messages = service.users().messages().list(maxResults=50, userId='me', q='in:inbox from:rbdundas@gmail.com').execute()
        messages = result_messages.get("messages", [])
        emails = []
        for message in messages:
            if message.get("id"):
                message = get_message(service, message.get("id"))
                emails.append(message)
    except HttpError as error:
        print(f"An error occurred: {error}")

    return render(request, "gmail.html", {"emails": emails})

import os
import base64
# import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# TODO: Logging, error handling, etc.
# TODO: Testing


class SendEmail:
    def __init__(self) -> None:
        # TODO: import all configuration, credentials, and authenticate.
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'examples/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def send_email(self, from_email: str, to_email: str, subject: str, message_body: str) -> bool:
        try:
            # Call the Gmail API
            gmail_service = build('gmail', 'v1', credentials=self.creds)
            email_content = (
                f"From: {from_email}\r\n"
                f"To: {to_email}\r\n"
                f"Subject: {subject}\r\n\r\n"
                f"{message_body}"
            )

            email_bytes = email_content.encode("utf-8")
            base64_encoded = base64.urlsafe_b64encode(email_bytes).decode()

            message = {
                'raw': base64_encoded
            }

            gmail_service.users().messages().send(userId='me', body=message).execute()
            print('Email sent successfully!')
            return True

        except HttpError as error:

            print(f'An error occurred: {error}')
            return False

    def read_template(self):
        # TODO: read the template file and return the contents
        pass

    def format_message(self):
        # TODO: format the message with the template and data
        pass

    def reauth(self):
        # TODO: If the token expires or does not have sufficent permissions, reauthenticate
        pass

'''# This script is used to scan the user's Gmail account to get app-related emails.'''
import os

from google.auth.credentials import AnonymousCredentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def authenticate_and_get_token():
    '''# Authenticate the user and get the token'''

    # The file token.json stores the user's access and refresh tokens
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    flow.redirect_uri = 'http://localhost:8080/'

    # Redirect user to Google's authentication page
    credentials = flow.run_local_server(port=8080)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

    return credentials

def authenticate_with_token(token):
    '''# Authenticate with the token and get the Gmail service'''
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", 'https://www.googleapis.com/auth/gmail.readonly')

    if not creds or not creds.valid:
        print("Can't authenticate with creds")
    service = build('gmail', 'v1', credentials=creds)
    return service

def scan_gmail(service):
    '''# Use the authenticated service to scan Gmail'''
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No labels found')
        return
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        subject = msg['payload']['headers'][16]['value']  # Adjust index as needed
        snippet = msg.get('snippet', '')
        print(f"Subject: {subject}, Snippet: {snippet}")


if __name__ == "__main__":
    '''# Main function to run the script'''
    # Step 1: Authenticate and get the token
    auth_token = authenticate_and_get_token()

    # Step 2: Authenticate with the obtained token
    gmail_service = authenticate_with_token(auth_token)

    # Step 3: Use the authenticated service to scan Gmail
    scan_gmail(gmail_service)

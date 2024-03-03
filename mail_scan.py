'''# This script is used to scan the user's Gmail account to get app-related emails.'''
from datetime import datetime

from flask import jsonify, session
from google.auth.api_key import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from CC24CWUT3.db_helpers.db_keywords import get_keywords, add_keyword
from CC24CWUT3.db_helpers.db_create_user import create_user


def are_credentials_expired():

    creds_json = session.get('creds')
    if creds_json:
        creds = Credentials.from_authorized_user_info(json.loads(creds_json))
        # Check if the credentials have an expiry attribute
        if creds.expiry is None:
            return True  # No expiry information, consider them expired

        # Check if the current time is beyond the credentials' expiry time
        return datetime.now() > creds.expiry


def get_gmail_service():
    # Retrieve credentials JSON from session
    creds_json = session.get('creds')

    if creds_json:
        # Deserialize JSON to Credentials object
        creds = Credentials.from_authorized_user_info(json.loads(creds_json))
        return build('gmail', 'v1', credentials=creds)

    return None


def authenticate_and_get_token():
    '''# Authenticate the user and get the token'''

    # The file token.json stores the user's access and refresh tokens
    scopes = ['https://www.googleapis.com/auth/gmail.readonly',\
               'https://www.googleapis.com/auth/userinfo.profile']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
    flow.redirect_uri = 'http://localhost:8080/'

    # Redirect user to Google's authentication page
    credentials = flow.run_local_server(port=8080)

    return credentials


def authenticate_with_token(creds):
    '''# Authenticate with the token and get the Gmail service'''

    #if the creds are not valid print an error
    if not creds or not creds.valid:
        print("Can't authenticate with creds")

    service = build('gmail', 'v1', credentials=creds)

    # get the user first/last from their gmail profile
    first, last = get_user_name(creds)
    print(first, last)

    secret = creds.client_secret
    print(secret)
    if first and last:
        try:
            create_user(secret, first, last)
        except Exception as e:
            print(e)

    return service, creds


def get_user_name(creds):
    """
    :param creds: OAuth token
    :return: strings first and last names.
    """
    try:
        service = build(serviceName="people", version="v1", credentials=creds)
        # Get the person details
        person = service.people().get(resourceName='people/me', personFields='names').execute()

        # Extract the first and last name
        if 'names' in person:
            for name in person['names']:
                if 'givenName' in name:
                    first = name['givenName']
                if 'familyName' in name:
                    last = name['familyName']

            return first, last
    except HttpError as e:
        print("Error while getting user first and last name!" + e)
        return None, None


def scan_gmail(service, client_id):
    '''
        Use the authenticated service to scan Gmail
        Go through new messages in box, send to analysis function
        then make list of lists [[classifier, email_body], [x, y], [x, y], ...]
        then return list of lists
    '''

    search_query = 'is:unread'
    results = service.users().messages().list(userId='me',q=search_query).execute()
    messages = results.get('messages', [])

    # list of list, first is classifier: 0, 1, -1 second is email body
    email_data = []
    if not messages:
        print('No labels found')
        return email_data

    # go through messages, check status and add to list
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        snippet = msg.get('snippet', '')
        status = determine_status(snippet, client_id)

        # add predicted status and email body to list of lists
        email_data.append([status, snippet])

    return jsonify(email_data)


def determine_status(snippet, clientId):
    """
     Determines with simple majority if message is good or bad based on keywords
    :return:
    """
    # print(snippet)
    # Keep track of the number of negative and positive words in email
    num_pos = 0
    num_neg = 0

    # Words is the words from email tokenized.
    words = snippet.split()

    neg_keywords = {"sorry", "regret", "candidate", "unfortunately"}
    pos_keywords = {"congratulations", "happy", "glad", "assessment", "invite"}
    keywords = get_keywords([clientId])

    # Go through the keywords from database. add them to the list
    for keyword in keywords:
        if keyword[1] == "POSITIVE":
            pos_keywords.add(keyword[0])
        else:
            neg_keywords.add(keyword[0])

    # Go through email words, inc num_neg/num_pos when appropriate
    for word in words:
        if word.lower() in neg_keywords:
            num_neg += 1
        if word.lower() in pos_keywords:
            num_pos += 1

    # Debug printing
    print("Num_pos", num_pos, "numneg", num_neg)

    # RETURNS (-1 : NEG, 1 : POS, 0 NEUTRAL)
    if num_neg > num_pos:
        return -1
    if num_pos > num_neg:
        return 1

    # Neutral
    return 0


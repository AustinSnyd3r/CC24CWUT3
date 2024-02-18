'''# This script is used to scan the user's Gmail account to get app-related emails.'''

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from CC24CWUT3.db_helpers.db_get_user import get_userid_by_oauth
from CC24CWUT3.db_helpers.db_keywords import get_keywords, add_keyword
from db_helpers.db_create_user import create_user

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
#
def authenticate_with_token(creds):
    '''# Authenticate with the token and get the Gmail service'''

    #if the creds are not valid print an error
    if not creds or not creds.valid:
        print("Can't authenticate with creds")

    service = build('gmail', 'v1', credentials=creds)

    #get the user first/last from their gmail profile
    first, last = get_user_name(creds)
    print(first, last)

    secret = creds.client_secret
    print(secret)
    if first and last:
        try:
            create_user(secret, first, last)
        except Exception as e:
            print(e)

    return service


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


def scan_gmail(service, clientId):
    '''# Use the authenticated service to scan Gmail'''
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No labels found')
        return
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        #subject = msg['payload']['headers'][16]['value']  # Adjust index as needed
        snippet = msg.get('snippet', '')
        print(determine_status(snippet, clientId))


def send_email_to_frontend(content):
    '''# Send the email content to the frontend'''
    print("This is a test")

def determine_status(snippet, clientId):
    """
     Determines with simple majority if message is good or bad based on keywords
    :param message:
    :return:
    """

    #keep track of the number of negative and positive words in email
    num_pos = 0
    num_neg = 0

    #words is the words from email tokenized.
    words = snippet.split()

    neg_keywords = {"sorry", "regret", "candidate", "unfortunately"}
    pos_keywords = {"congratulations", "happy", "glad", "assessment", "invite"}
    keywords = get_keywords([clientId])

    #go through the keywords from database. add them to the list
    for keyword in keywords:
        if keyword[1] == "POSITIVE":
            pos_keywords.add(keyword[0])
        else:
            neg_keywords.add(keyword[0])

    #Go through email words, inc num_neg/num_pos when appropriate
    for word in words:
        if word.lower() in neg_keywords:
            num_neg += 1
        if word.lower() in pos_keywords:
            num_pos += 1

    #debug printing
    print("Num_pos", num_pos, "numneg", num_neg)

    #RETURNS (-1 : NEG, 1 : POS, 0 NEUTRAL)
    if num_neg > num_pos:
        return -1
    else:
        if num_pos > num_neg:
            return 1
        else:
            return 0


if __name__ == "__main__":
    # Step 1: Authenticate and get the token
    auth_token = authenticate_and_get_token()

    # Step 2: get the client id. we want to reduce passing the token around
    clientId = get_userid_by_oauth([auth_token.client_secret])

    # Step 2: Authenticate with the obtained token
    gmail_service = authenticate_with_token(auth_token)

    # Step 3: Use the authenticated service to scan Gmail
    scan_gmail(gmail_service, clientId)

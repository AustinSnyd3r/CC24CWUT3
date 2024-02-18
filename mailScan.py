'''# This script is used to scan the user's Gmail account to get app-related emails.'''

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
#from CC24CWUT3.db_helpers.db_create_user import create_user
#from CC24CWUT3.db_helpers.db_keywords import get_keywords

def authenticate_and_get_token():
    '''# Authenticate the user and get the token'''

    # The file token.json stores the user's access and refresh tokens
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.profile']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
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
    first, last = getUserName(creds)
    print(first, last)
    #if first and last:
        # TODO: This might not be right to pass as the token
        #create_user(creds, first, last)

    return service


def getUserName(creds):
    """

    :param creds: OAuth token
    :return: strings first and last names.
    """
    try:
        service = build("people", "v1", credentials=creds)
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
    except Exception as e:
        print("Error while getting user first and last name!" + e)
        return None, None


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
        print(determineStatus(snippet))


def determineStatus(snippet):
    """
     Determines with simple majority if message is good or bad based on keywords
    :param message:
    :return:
    """

    numPos = 0
    numNeg = 0

    words = snippet.split()
    #TODO: Make this work with individual users keywords

    negKeywords = {"sorry", "regret", "candidate", "unfortunately"}
    posKeywords = {"congratulations", "happy", "glad", "assessment", "invite"}

    for word in words:
        if word.lower() in negKeywords:
            numNeg += 1
        if word.lower() in posKeywords:
            numPos += 1

    if numNeg > numPos:
        return -1
    if numPos > numNeg:
        return 1
    else:
        return 0


if __name__ == "__main__":
    '''# Main function to run the script'''
    # Step 1: Authenticate and get the token
    auth_token = authenticate_and_get_token()

    # Step 2: Authenticate with the obtained token
    gmail_service = authenticate_with_token(auth_token)

    # Step 3: Use the authenticated service to scan Gmail
    scan_gmail(gmail_service)

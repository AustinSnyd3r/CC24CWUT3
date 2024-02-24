from flask import Flask, render_template, jsonify
from flask_cors import CORS

from CC24CWUT3.db_helpers.db_create_app import create_app
from CC24CWUT3.db_helpers.db_get_user import get_userid_by_oauth
from CC24CWUT3.db_helpers.db_update_app import get_app_by_id
from CC24CWUT3.mail_scan import authenticate_and_get_token, authenticate_with_token, scan_gmail

app = Flask(__name__)
CORS(app)

#Global client id to keep track of user using the app
global client_id

@app.route('/')
def oauth_verification():
    # Step 1: Authenticate and get the token
    auth_token = authenticate_and_get_token()

    # Step 2: Get the client id. We want to reduce passing the token around
    global client_id
    client_id = get_userid_by_oauth([auth_token.client_secret])
    # Step 3: Authenticate with the obtained token
    gmail_service = authenticate_with_token(auth_token)

    # Step 4: Use the authenticated service to scan Gmail
    scan_gmail(gmail_service, client_id)

    return render_template('index.html', static_url_path='/static')

@app.route("/loadFakeData")
def loadFakeData():
    global client_id
    create_app("Facebook", "SWE Intern", [client_id])
    create_app("Amazon", "UI Intern", [client_id])
    create_app("Microsoft", "Frontend Intern", [client_id])
    create_app("Google", "Senior SWE", [client_id])
    return render_template('index.html', static_url_path='/static')

def get_applications(id):
    """# Retrieves the applications for a given user
         Returns json of the applications
    """
    print((get_app_by_id(id)))
    return jsonify(get_app_by_id(id))

@app.route("/applications")
def test_applications():
    global client_id
    return get_applications(client_id)

if __name__ == '__main__':

    app.run(debug=True)
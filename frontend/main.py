import os

from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, session
from flask_cors import CORS

from CC24CWUT3.db_helpers.db_create_app import create_app
from CC24CWUT3.db_helpers.db_get_user import get_userid_by_oauth
from CC24CWUT3.db_helpers.db_update_app import get_app_by_id
from CC24CWUT3.mail_scan import authenticate_and_get_token, authenticate_with_token, scan_gmail

load_dotenv('key.env')
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

@app.route('/')
def oauth_verification():
    # Step 1: Authenticate and get the token
    auth_token = authenticate_and_get_token()

    # Step 2: Get the client id. We want to reduce passing the token around
    client_id = get_userid_by_oauth([auth_token.client_secret])
    session['client_id'] = client_id

    # Step 3: Authenticate with the obtained token
    gmail_service = authenticate_with_token(auth_token)

    # Step 4: Use the authenticated service to scan Gmail
    scan_gmail(gmail_service, client_id)

    return render_template('index.html', static_url_path='/static')

@app.route("/loadFakeData")
def loadFakeData():
    client_id = session.get('client_id')
    create_app("Facebook", "SWE Intern", [client_id])
    create_app("Amazon", "UI Intern", [client_id])
    create_app("Microsoft", "Frontend Intern", [client_id])
    create_app("Google", "Senior SWE", [client_id])
    return render_template('index.html', static_url_path='/static')

@app.route("/applications")
def get_applications():
    """# Retrieves the applications for a given user
             Returns json of the applications
        """
    client_id = session.get('client_id')

    return jsonify(get_app_by_id(client_id))

if __name__ == '__main__':

    app.run(debug=True)
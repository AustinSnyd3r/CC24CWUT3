import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, session, url_for, redirect
from flask_cors import CORS
from CC24CWUT3.db_helpers.db_create_app import create_app
from CC24CWUT3.db_helpers.db_get_user import get_userid_by_oauth
from CC24CWUT3.db_helpers.db_update_app import get_app_by_id, delete_app_by_id, update_whole_app
from CC24CWUT3.mail_scan import authenticate_and_get_token, authenticate_with_token, scan_gmail

load_dotenv('key.env')
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')


def is_user_authenticated():
    """Checks if the user has authenticated to reduce need to sign in multiple times"""
    return 'client_id' in session


@app.route('/')
def oauth_verification():
    """Verifies OAuth for Google Mail API. Saves the client id to env variable
       returns the home html page.
    """
    # Check if the user is already authenticated
    if not is_user_authenticated():
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



@app.route("/emails")
def emails():
    return render_template('emails.html', static_url_path='/static')


@app.route("/home")
def home_page():
    return redirect('index.html', static_url_path='/static')


@app.route("/loadFakeData")
def loadFakeData():
    """Just meant for testing purposes"""
    client_id = session.get('client_id')
    create_app("Facebook", "SWE Intern", "WAITING", [client_id])
    create_app("Amazon", "UI Intern", "WAITING", [client_id])
    create_app("Microsoft", "Frontend Intern", "WAITING", [client_id])
    create_app("Google", "Senior SWE", "WAITING", [client_id])
    return render_template('index.html', static_url_path='/static')


@app.route("/applications")
def get_applications():
    """# Retrieves the applications for a given user
             Returns json of the applications
        """
    client_id = session.get('client_id')

    return jsonify(get_app_by_id(client_id))


@app.route("/applications/delete/<app_id>", methods=['DELETE'])
def delete_application(app_id):
    """Used to delete application from database by id. calls method in db_helpers"""
    try:
        client_id = session.get('client_id')
        delete_app_by_id(app_id, client_id)
        return 'Success', 200
    except Exception as e:
        print(f"Error deleting application with ID {app_id}: {e}")
        return 'Failed', 500


@app.route("/applications/edit/<company>/<position>/<status>/<app_id>", methods=['GET'])
def edit_application(company, position, status, app_id):

    """Used to edit an existing application by calling method in db_helpers"""
    client_id = session.get('client_id')
    try:
        update_whole_app(company, position, status, app_id, client_id)
        return "Success", 200
    except Exception as e:
        print("Error updating application with id:", app_id, e)
        return "Error updating application", 500


@app.route("/applications/add/<company>/<position>/<status>")
def add_application(company, position, status):
    """Used to add an application to database. Calls create_app from db_helpers."""
    try:
        client_id = session.get('client_id')
        create_app(company, position, status, [client_id])
        return 'Success', 200
    except Exception as e:
        print("Error adding application to database", e)
        return "Error adding application", 500


if __name__ == '__main__':
    app.run(debug=True)
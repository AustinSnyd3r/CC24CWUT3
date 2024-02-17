import json
import os
from pathlib import Path
import uuid

import db_helpers.db_connection as db_conn

# Load our database configurations from the config file
DB_CONFIGS = None
parent_dir = Path(__file__).resolve().parents[1]
config_path = os.path.join(str(parent_dir), "/config/db_config.json")
config_file = open(config_path)
DB_CONFIGS = json.load(config_file)
config_file.close()

# Extract the database configurations
user = DB_CONFIGS['user']
password = DB_CONFIGS['password']
host = DB_CONFIGS['host']
database = DB_CONFIGS['database']

# Create a new MySqlConnection object
sql_conn = db_conn.MySqlConnection(host, user, password, database)

# Create a new user with the given clientid, clientoauth, firstname, and lastname
def create_user(clientid, clientoauth, firstname, lastname):
    conn = db_conn.get_connection()
    conn.connect()

    sql = "INSERT INTO users (clientid, clientoauth, firstname, lastname) VALUES (%s, %s, %s, %s)"
    data = (clientid, clientoauth, firstname, lastname)

    conn.execute_update(sql, data)
    conn.disconnect()

# Create a new user with a random clientid and the given clientoauth, firstname, and lastname
def create_user(clientoauth, firstname, lastname):
    unique_clientid = uuid.uuid4()

    conn = db_conn.get_connection()

    create_user(unique_clientid, clientoauth, firstname, lastname)
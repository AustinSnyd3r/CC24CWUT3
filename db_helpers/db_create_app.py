from datetime import date
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

# Creates a new application with the given company/position
def create_app(company, position, userid):
    conn = db_conn.MySqlConnection(host, user, password, database)
    conn.connect()

    check_sql = "SELECT * FROM users WHERE userid = %s"
    check_data = (userid)
    check_result = conn.execute_select(check_sql, check_data)
    if len(check_result) == 0:
        conn.disconnect()
        raise ValueError("Invalid userid provided to create_app.")

    sql = "INSERT INTO applications (clientid, company, position, status, date_submitted) VALUES (%s, %s, %s, %s, %s)"
    data = (userid, company, position, "WAITING", date.today())

    conn.execute_update(sql, data)
    conn.disconnect()
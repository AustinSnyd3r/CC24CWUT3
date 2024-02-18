import json
import os
from pathlib import Path

import db_helpers.db_connection as db_conn

# Get a user from their oauth token
def get_user_by_oauth(oauth):
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "SELECT * FROM users WHERE oauth = %s"
    data = (oauth)

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

def get_user_by_userid(userid):
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "SELECT * FROM users WHERE userid = %s"
    data = (userid)

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

def get_userid_by_oauth(oauth):
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "SELECT userid FROM users WHERE oauth = %s"
    data = (oauth)

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result[0][0]

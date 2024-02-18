'''# Purpose: Contains the functions to get a user from the database'''
import json
import os
from pathlib import Path

import db_connection as db_conn

def get_user_by_oauth(oauth):
    '''# Get a user from their oauth token'''
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "SELECT * FROM users WHERE oauth = %s"
    data = (oauth)

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

def get_user_by_userid(userid):
    '''# Get a user from their userid'''
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "SELECT * FROM users WHERE userid = %s"
    data = (userid)

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

def get_userid_by_oauth(oauth):
    '''# Get a user's id from their oauth token'''
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "SELECT userid FROM users WHERE oauth = %s"
    data = (oauth)

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result[0][0]

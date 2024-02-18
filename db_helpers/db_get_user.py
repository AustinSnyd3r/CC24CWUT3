'''# Purpose: Contains the functions to get a user from the database'''

from db_helpers.db_connection import SQLConnection

def get_user_by_oauth(oauth):
    '''# Get a user from their oauth token'''
    conn = SQLConnection()
    conn.connect()

    sql = "SELECT * FROM users WHERE oauth = %s"
    data = oauth

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

def get_user_by_userid(userid):
    '''# Get a user from their userid'''
    conn = SQLConnection()
    conn.connect()

    sql = "SELECT * FROM users WHERE clientid = %s"
    data = userid

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

def get_userid_by_oauth(oauth):
    '''# Get a user's id from their oauth token'''
    conn = SQLConnection()
    conn.connect()

    sql = "SELECT clientid FROM clients WHERE clientoauth = %s"
    data = oauth

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result[0][0]

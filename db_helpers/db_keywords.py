'''# Purpose: Contains functions to manipulate the keywords table in the database'''
from CC24CWUT3.db_helpers.db_connection import SQLConnection

valid_keyword_types = ["NEGATIVE", "POSITIVE", "INTERVIEW", "OFFER", "REJECTED", "ACCEPTED"]

def add_keyword(clientid, keyword, keywordtype):
    '''# Add a keyword to the database'''
    conn = SQLConnection()
    conn.connect()

    sql = "INSERT INTO keywords (clientid, keyword, keywordtype) VALUES (%s, %s, %s)"
    data = (clientid, keyword, keywordtype)

    conn.execute_update(sql, data)
    conn.disconnect()

def update_keyword_category(clientid, keyword, keywordtype):
    '''# Update a keyword's category'''
    conn = SQLConnection()
    conn.connect()

    if keywordtype not in valid_keyword_types:
        conn.disconnect()
        raise ValueError("Invalid keyword type provided to update_keyword_category.")

    sql = "UPDATE keywords SET keywordtype = %s WHERE clientid = %s AND keyword = %s"
    data = (keywordtype, clientid, keyword)

    conn.execute_update(sql, data)
    conn.disconnect()

def get_keywords(clientid):
    '''# Get all keywords for a user, along with their categories'''
    conn = SQLConnection()
    conn.connect()

    sql = "SELECT keyword, keywordtype FROM keywords WHERE clientid = %s"
    data = clientid

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

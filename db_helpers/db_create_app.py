'''# Purpose: Contains the function to create a new application in the database.'''
from datetime import date

from CC24CWUT3.db_helpers.db_connection import SQLConnection

def create_app(company, position, status, userid):
    '''# Creates a new application with the given company/position'''
    conn = SQLConnection()
    conn.connect()

    check_sql = "SELECT * FROM clients WHERE clientid = %s"
    check_data = userid
    check_result = conn.execute_select(check_sql, check_data)
    if len(check_result) == 0:
        conn.disconnect()
        raise ValueError("Invalid userid provided to create_app.")

    sql = "INSERT INTO applications (clientid, company, position, \
        status, date_submitted) VALUES (%s, %s, %s, %s, %s)"
    userid = userid[0]
    data = (userid, company, position, status, date.today())

    conn.execute_update(sql, data)
    conn.disconnect()

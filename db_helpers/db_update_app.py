'''# Purpose: Contains functions to manipulate the applications table in the database'''

from CC24CWUT3.db_helpers.db_connection import SQLConnection

valid_statuses = ["WAITING", "REJECTED", "INTERVIEW", "OFFER", "ACCEPTED"]
class InvalidStatusError(ValueError):
    '''# Status handling'''

def update_company_name(app_id, new_name):
    '''# Update a company name'''
    conn = SQLConnection()
    conn.connect()

    sql = "UPDATE applications SET company = %s WHERE applicationid = %s"
    data = (new_name, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def update_position_name(app_id, new_name):
    '''# Update a position name'''
    conn = SQLConnection()
    conn.connect()

    sql = "UPDATE applications SET position = %s WHERE applicationid = %s"
    data = (new_name, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def update_status(app_id, new_status):
    '''# Update the status of an application'''
    if new_status not in valid_statuses:
        raise InvalidStatusError("Invalid status provided to update_status.")

    conn = SQLConnection()
    conn.connect()

    sql = "UPDATE applications SET status = %s WHERE applicationid = %s"
    data = (new_status, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def notify_update(app_id):
    '''# Set the update flag for an application'''
    conn = SQLConnection()
    conn.connect()

    sql = "UPDATE applications SET has_update = 1 WHERE applicationid = %s"
    data = app_id

    conn.execute_update(sql, data)
    conn.disconnect()

def clear_update(app_id):
    '''# Clear the update flag for an application'''
    conn = SQLConnection()
    conn.connect()

    sql = "UPDATE applications SET has_update = 0 WHERE applicationid = %s"
    data = app_id

    conn.execute_update(sql, data)
    conn.disconnect()

def get_app_by_id(clientid):
    '''# Select all the applications for a given clientid '''
    conn = SQLConnection()
    conn.connect()

    sql = "SELECT * FROM applications WHERE clientid = %s"
    data = [clientid]

    result = conn.execute_select(sql, data)
    conn.disconnect()

    return result

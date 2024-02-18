'''# Purpose: Contains functions to manipulate the applications table in the database'''
import json
import os
from pathlib import Path

import db_connection as db_conn

'''# Status handling'''
valid_statuses = ["WAITING", "REJECTED", "INTERVIEW", "OFFER", "ACCEPTED"]
class InvalidStatusError(ValueError):
    pass

'''# Update a company name'''
def update_company_name(app_id, new_name):
    conn = db_conn.my_sql_connection()
    conn.connect()

    sql = "UPDATE applications SET company = %s WHERE applicationid = %s"
    data = (new_name, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

'''# Update a position name'''
def update_position_name(app_id, new_name):
    conn = db_conn.my_sql_connection()
    conn.connect()

    sql = "UPDATE applications SET position = %s WHERE applicationid = %s"
    data = (new_name, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

'''# Update the status of an application'''
def update_status(app_id, new_status):
    if new_status not in valid_statuses:
        raise InvalidStatusError("Invalid status provided to update_status.")

    conn = db_conn.my_sql_connection()
    conn.connect()

    sql = "UPDATE applications SET status = %s WHERE applicationid = %s"
    data = (new_status, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

'''# Set the update flag for an application'''
def notify_update(app_id):
    conn = db_conn.my_sql_connection()
    conn.connect()

    sql = "UPDATE applications SET has_update = 1 WHERE applicationid = %s"
    data = (app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

'''# Clear the update flag for an application'''
def clear_update(app_id):
    conn = db_conn.my_sql_connection()
    conn.connect()

    sql = "UPDATE applications SET has_update = 0 WHERE applicationid = %s"
    data = (app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

'''# Purpose: Contains functions to manipulate the applications table in the database'''
import json
import os
from pathlib import Path

from db_helpers.db_connection import MySqlConnection

valid_statuses = ["WAITING", "REJECTED", "INTERVIEW", "OFFER", "ACCEPTED"]
class InvalidStatusError(ValueError):
    '''# Status handling'''
    pass

def update_company_name(app_id, new_name):
    '''# Update a company name'''
    conn = MySqlConnection()
    conn.connect()

    sql = "UPDATE applications SET company = %s WHERE applicationid = %s"
    data = (new_name, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def update_position_name(app_id, new_name):
    '''# Update a position name'''
    conn = MySqlConnection()
    conn.connect()

    sql = "UPDATE applications SET position = %s WHERE applicationid = %s"
    data = (new_name, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def update_status(app_id, new_status):
    '''# Update the status of an application'''
    if new_status not in valid_statuses:
        raise InvalidStatusError("Invalid status provided to update_status.")

    conn = MySqlConnection()
    conn.connect()

    sql = "UPDATE applications SET status = %s WHERE applicationid = %s"
    data = (new_status, app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def notify_update(app_id):
    '''# Set the update flag for an application'''
    conn = MySqlConnection()
    conn.connect()

    sql = "UPDATE applications SET has_update = 1 WHERE applicationid = %s"
    data = (app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

def clear_update(app_id):
    '''# Clear the update flag for an application'''
    conn = MySqlConnection()
    conn.connect()

    sql = "UPDATE applications SET has_update = 0 WHERE applicationid = %s"
    data = (app_id)

    conn.execute_update(sql, data)
    conn.disconnect()

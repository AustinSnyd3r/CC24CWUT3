"""
# Purpose: Contains the function to create a new user in the database
"""
import uuid

import db_connection as db_conn

"""
# Raised if we can't create a clientid for a new user
"""
class ClientCreationError(ValueError):
    pass

"""
# Create a new user with the given clientid, clientoauth, firstname, and lastname
"""
def create_user(clientid, clientoauth, firstname, lastname):
    conn = db_conn.my_sql_connection()
    conn.connect()

    sql = "INSERT INTO users (clientid, clientoauth, firstname, lastname) VALUES (%s, %s, %s, %s)"
    data = (clientid, clientoauth, firstname, lastname)

    conn.execute_update(sql, data)
    conn.disconnect()

"""
# Create a new user with a random clientid and the given clientoauth, firstname, and lastname
"""
def create_user(clientoauth, firstname, lastname):
    unique_clientid = uuid.uuid4()
    conn = db_conn.my_sql_connection()
    conn.connect()
    id_found = False
    sql = "SELECT clientid FROM users WHERE clientid = %s"
    data = (unique_clientid)
    result = conn.execute_select(sql, data)
    if len(result) > 0:
        id_found = True
    tries = 0
    while id_found:
        unique_clientid = uuid.uuid4()
        data = (unique_clientid)
        result = conn.execute_select(sql, data)
        if len(result) == 0:
            id_found = False
        tries += 1
        if tries > 10:
            conn.disconnect()
            raise ClientCreationError("Unable to generate a unique clientid for the new user.")

    create_user(clientid = unique_clientid, clientoauth = clientoauth, firstname = firstname, lastname = lastname)

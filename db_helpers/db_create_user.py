'''# Purpose: Contains the function to create a new user in the database'''
import uuid

from db_helpers.db_connection import SQLConnection


class ClientCreationError(ValueError):
    '''# Raised if we can't create a clientid for a new user'''
    pass

def create_user(clientoauth, firstname, lastname):
    '''# Create a new user with a random clientid and the given clientoauth, \
    firstname, and lastname'''
    unique_clientid = str(uuid.uuid4())
    conn = SQLConnection()
    conn.connect()
    id_found = False
    sql = "SELECT clientid FROM clients WHERE clientid = %s"
    data = unique_clientid
    data = [data]
    result = conn.execute_select(sql, data)
    if result is not None and len(result) > 0:
        id_found = True
    tries = 0
    while id_found:
        unique_clientid = str(uuid.uuid4())
        data = [unique_clientid]
        result = conn.execute_select(sql, data)
        if result is None or len(result) == 0:
            id_found = False
        tries += 1
        if tries > 10:
            conn.disconnect()
            raise ClientCreationError("Unable to generate a unique clientid \
                                      for the new user.")

    sql = "INSERT INTO clientids (clientid) VALUES (%s)"
    data = unique_clientid
    data = [data]
    conn.execute_update(sql, data)

    sql = "INSERT INTO clients (clientid, clientoauth, firstname, \
        lastname) VALUES (%s, %s, %s, %s)"
    data = (unique_clientid, clientoauth, firstname, lastname)

    conn.execute_update(sql, data)
    conn.disconnect()

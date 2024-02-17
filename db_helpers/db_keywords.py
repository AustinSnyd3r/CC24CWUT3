import db_helpers.db_connection as db_conn

# Add a keyword to the database
def add_keyword(clientid, keyword, keywordtype):
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "INSERT INTO keywords (clientid, keyword, keywordtype) VALUES (%s, %s, %s)"
    data = (clientid, keyword, keywordtype)

    conn.execute_update(sql, data)
    conn.disconnect()

# Update a keyword's category
def update_keyword_category(clientid, keyword, keywordtype):
    conn = db_conn.MySqlConnection()
    conn.connect()

    sql = "UPDATE keywords SET keywordtype = %s WHERE clientid = %s AND keyword = %s"
    data = (keywordtype, clientid, keyword)

    conn.execute_update(sql, data)
    conn.disconnect()
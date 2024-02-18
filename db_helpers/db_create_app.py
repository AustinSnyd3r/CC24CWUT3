from datetime import date

import db_helpers.db_connection as db_conn

# Creates a new application with the given company/position
def create_app(company, position, userid):
    conn = db_conn.MySqlConnection()
    conn.connect()

    check_sql = "SELECT * FROM users WHERE userid = %s"
    check_data = (userid)
    check_result = conn.execute_select(check_sql, check_data)
    if len(check_result) == 0:
        conn.disconnect()
        raise ValueError("Invalid userid provided to create_app.")

    sql = "INSERT INTO applications (clientid, company, position, status, date_submitted) VALUES (%s, %s, %s, %s, %s)"
    data = (userid, company, position, "WAITING", date.today())

    conn.execute_update(sql, data)
    conn.disconnect()
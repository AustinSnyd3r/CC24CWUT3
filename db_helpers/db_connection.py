# Purpose: Used to establish a connection to a MySQL database and provide methods to execute SQL queries
import json
import os
from pathlib import Path

import mysql.connector

# Stores an SQL connection, providing interface methods that perform SQL sanitization and error handling
class my_sql_connection:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def __init__(self):
        # Load our database configurations from the config file
        db_configs = None
        parent_dir = Path(__file__).resolve().parents[1]
        config_path = os.path.join(str(parent_dir), "/config/db_config.json")
        with open(config_path, "r") as config_file:
            db_configs = json.load(config_file)
        # Extract the database configurations
        self.host = db_configs['host']
        self.username = db_configs['user']
        self.password = db_configs['password']
        self.database = db_configs['database']
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL database")
        else:
            print("No active connection to close")

    def execute_update(self, sql, data=None):
        if not self.connection:
            print("No active connection. Please connect first.")
            return

        # Escape characters to prevent SQL injection
        for i in enumerate(data):
            data[i] = self.connection.escape_string(data[i])

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            cursor.close()
            print("Update executed successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def execute_select(self, sql, data=None):
        if not self.connection:
            print("No active connection. Please connect first.")
            return None

        # Escape characters to prevent SQL injection
        for i in range(len(data)):
            data[i] = self.connection.escape_string(data[i])

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

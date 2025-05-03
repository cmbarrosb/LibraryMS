# Imports
# mysql.connector: MySQL driver for Python
# os: for file path operations
# getpass: for secure password input
import mysql.connector
import os
import getpass

# Prompt the user for MySQL connection details
def prompt_credentials():
    host = input("Host [localhost]: ") or "localhost"
    user = input("Username [root]: ") or "root"
    password = getpass.getpass("Password: ")
    database = input("Database [library_db]: ") or "library_db"
    return host, user, password, database

# Open a connection to the MySQL server using provided credentials
def open_connection(host, user, password):
    config = {'host': host, 'user': user, 'password': password}
    return mysql.connector.connect(**config)

# Execute SQL commands from a .sql file, splitting on semicolons
# Print any errors along with the failed command for debugging
def run_sql_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print(f"Failed command: {command}\n")

# Initialize the database: select DB
def initialize_database(cursor, database):
    cursor.execute(f"USE {database};")

# Load schema and data SQL files unconditionally
def load_sql_files(cursor, schema_path, data_path):
    print("Running schema.sql...")
    run_sql_file(cursor, schema_path)
    print("Running data.sql...")
    run_sql_file(cursor, data_path)

# Main orchestration: prompt credentials, connect, initialize, load SQL, and cleanup
def main():
    print("Enter your MySQL login details")
    host, user, password, database = prompt_credentials()

    # Establish a database connection and create a cursor
    try:
        connection = open_connection(host, user, password)
        cursor = connection.cursor()

        initialize_database(cursor, database)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, '..', 'sql', 'schema.sql')
        data_path = os.path.join(current_dir, '..', 'sql', 'data.sql')

        load_sql_files(cursor, schema_path, data_path)

        # Commit all changes
        connection.commit()
        print("Database initialized successfully!")

    # Handle any connection or execution errors gracefully
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")

    # Ensure resources are cleaned up by closing cursor and connection
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Connection closed.")

if __name__ == '__main__':
    main()

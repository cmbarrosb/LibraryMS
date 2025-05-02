import mysql.connector
import os
import getpass

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

def main():
    connection = None

    print("Enter your MySQL login details")
    host = input("Host [localhost]: ") or "localhost"
    user = input("Username [root]: ") or "root"
    password = getpass.getpass("Password: ")
    database = input("Database [library_db]: ") or "library_db"
    reset_flag = input("Reset database? (y/N): ").strip().lower() == 'y'

    config = {
        'host': host,
        'user': user,
        'password': password
    }

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        if reset_flag:
            # Reset database to a clean state
            cursor.execute(f"DROP DATABASE IF EXISTS {database};")
            cursor.execute(f"CREATE DATABASE {database};")
        cursor.execute(f"USE {database};")
        # Disable foreign key checks for bulk loading
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, '..', 'sql', 'schema.sql')
        data_path = os.path.join(current_dir, '..', 'sql', 'data.sql')

        if reset_flag:
            print("Running schema.sql...")
            run_sql_file(cursor, schema_path)

            print("Running data.sql...")
            run_sql_file(cursor, data_path)
        else:
            print("Skipping schema and data load (no reset)")

        connection.commit()
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("Database initialized successfully!")

    except mysql.connector.Error as err:
        print(f"Connection error: {err}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Connection closed.")

if __name__ == '__main__':
    main()

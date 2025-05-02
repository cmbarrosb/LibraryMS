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

    print("🔐 Enter your MySQL login details")
    host = input("Host [localhost]: ") or "localhost"
    user = input("Username [root]: ") or "root"
    password = getpass.getpass("Password: ")
    database = input("Database [library_db]: ") or "library_db"

    config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, '..', 'sql', 'schema.sql')
        data_path = os.path.join(current_dir, '..', 'sql', 'data.sql')

        print("📘 Running schema.sql...")
        run_sql_file(cursor, schema_path)

        print("📗 Running data.sql...")
        run_sql_file(cursor, data_path)

        connection.commit()
        print("✅ Database initialized successfully!")

    except mysql.connector.Error as err:
        print(f"❌ Connection error: {err}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Connection closed.")

if __name__ == '__main__':
    main()

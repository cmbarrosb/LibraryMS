

import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime, timedelta

# Module‐level connection
_conn = None

def prompt_credentials():
    """Prompt only for the database password; use defaults for host/user/db."""
    host = "localhost"
    user = "root"
    database = "library_db"
    password = getpass.getpass("MySQL password for root@localhost: ")
    return host, user, password, database

def open_connection(host, user, password, database):
    """Open and return a new DB connection."""
    config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }
    return mysql.connector.connect(**config)

def get_connection():
    """Return the existing connection or error if uninitialized."""
    global _conn
    if _conn is None:
        raise RuntimeError("Connection not initialized. Call main() first.")
    return _conn

def print_table(rows):
    """Print a list of dicts as a simple aligned table with friendly headers."""
    if not rows:
        print("No records found.")
        return

    headers = list(rows[0].keys())
    # Map raw column names to user-friendly labels
    header_map = {
        'loan_id': 'Loan #',
        'member_id': 'Member #',
        'name': 'Name',
        'ssn': 'SSN',
        'address': 'Address',
        'expiration_date': 'Expiration Date',
        'active_flag': 'Active',
        'professor_privileges': 'Privileges',
        'isbn': 'ISBN',
        'title': 'Title',
        'subject': 'Subject',
        'author': 'Author',
        'description': 'Description',
        'copy_id': 'Copy ID',
        'status': 'Status',
        'location': 'Location',
        'checkout_date': 'Checkout Date',
        'due_date': 'Due Date',
        'return_date': 'Return Date',
        'overdue_status': 'Overdue Status',
        'staff_id': 'Staff ID',
        'staff_name': 'Staff Name',
        'staff_role': 'Role'
    }
    # Prepare display headers using the mapping
    display_headers = [header_map.get(h, h) for h in headers]

    # Compute column widths
    widths = {}
    for h, dh in zip(headers, display_headers):
        max_data = max(len(str(r[h])) for r in rows)
        widths[h] = max(len(dh), max_data)

    # Print header row
    header_line = " | ".join(dh.ljust(widths[h]) for h, dh in zip(headers, display_headers))
    print(header_line)
    print("-" * len(header_line))

    # Print data rows
    for r in rows:
        line = " | ".join(str(r[h]).ljust(widths[h]) for h in headers)
        print(line)

def add_record_menu():
    """Placeholder: implement Add Book/Copy/Member/Staff here."""
    print("Add Record submenu (to be implemented)")

def get_menu():
    """Placeholder: implement Get by ID and List submenu here."""
    print("Get Record submenu (to be implemented)")

def update_menu():
    """Placeholder: implement Update and Delete submenu here."""
    print("Update Record submenu (to be implemented)")

def main():
    """Top‐level action menu: Add, Get, or Update (0 to exit)."""
    global _conn
    host, user, password, database = prompt_credentials()
    _conn = open_connection(host, user, password, database)

    while True:
        print("\nWelcome to the Library Management System!")
        print("1) Add Record")
        print("2) Get Record")
        print("3) Update Record")
        choice = input("Select an action (0 to exit): ").strip()

        if choice == "0":
            print("Goodbye!")
            if _conn:
                _conn.close()
            break
        elif choice == "1":
            add_record_menu()
        elif choice == "2":
            get_menu()
        elif choice == "3":
            update_menu()
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()


import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime, timedelta

# Module-level connection (initialized on first use)
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
    """Return a persistent connection, prompting credentials on first call."""
    global _conn
    if _conn is None:
        host, user, password, database = prompt_credentials()
        _conn = open_connection(host, user, password, database)
    return _conn


# --- Helper: Print Table ---
def print_table(rows):
    """Print a list of dicts as a simple aligned table with friendly headers."""
    if not rows:
        print("No records found.")
        return

    headers = list(rows[0].keys())
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

# --- Book CRUD ---

def add_book(isbn, title, subject, author, description):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT IGNORE INTO Book "
           "(isbn, title, subject, author, description) "
           "VALUES (%s, %s, %s, %s, %s)")
    try:
        cursor.execute(sql, (isbn, title, subject, author, description))
        conn.commit()
        return True
    except Error as e:
        print("Error adding book:", e)
        return False
    finally:
        cursor.close()

def get_book(isbn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Book WHERE isbn = %s", (isbn,))
        return cursor.fetchone()
    except Error as e:
        print("Error fetching book:", e)
        return None
    finally:
        cursor.close()

def list_books(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Book LIMIT %s", (limit,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing books:", e)
        return []
    finally:
        cursor.close()

def update_book(isbn, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    fields = ", ".join(f"{col} = %s" for col in kwargs)
    values = list(kwargs.values()) + [isbn]
    sql = f"UPDATE Book SET {fields} WHERE isbn = %s"
    try:
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error updating book:", e)
        return False
    finally:
        cursor.close()

def delete_book(isbn):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Book WHERE isbn = %s", (isbn,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error deleting book:", e)
        return False
    finally:
        cursor.close()

# --- Copy CRUD ---

def add_copy(isbn, copy_id, status, location):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT IGNORE INTO Copy (isbn, copy_id, status, location) "
           "VALUES (%s, %s, %s, %s)")
    try:
        cursor.execute(sql, (isbn, copy_id, status, location))
        conn.commit()
        return True
    except Error as e:
        print("Error adding copy:", e)
        return False
    finally:
        cursor.close()

def get_copy(isbn, copy_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Copy WHERE isbn = %s AND copy_id = %s", (isbn, copy_id))
        return cursor.fetchone()
    except Error as e:
        print("Error fetching copy:", e)
        return None
    finally:
        cursor.close()

def list_copies(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Copy LIMIT %s", (limit,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing copies:", e)
        return []
    finally:
        cursor.close()

def update_copy(isbn, copy_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    fields = ", ".join(f"{col} = %s" for col in kwargs)
    values = list(kwargs.values()) + [isbn, copy_id]
    sql = f"UPDATE Copy SET {fields} WHERE isbn = %s AND copy_id = %s"
    try:
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error updating copy:", e)
        return False
    finally:
        cursor.close()

def delete_copy(isbn, copy_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Copy WHERE isbn = %s AND copy_id = %s", (isbn, copy_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error deleting copy:", e)
        return False
    finally:
        cursor.close()

# --- Member CRUD ---

def add_member(member_id, name, ssn, address, expiration_date, active_flag, professor_privileges):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT IGNORE INTO Member (member_id, name, ssn, address, expiration_date, active_flag, professor_privileges) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    try:
        cursor.execute(sql, (member_id, name, ssn, address, expiration_date, active_flag, professor_privileges))
        conn.commit()
        return True
    except Error as e:
        print("Error adding member:", e)
        return False
    finally:
        cursor.close()

def get_member(member_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Member WHERE member_id = %s", (member_id,))
        return cursor.fetchone()
    except Error as e:
        print("Error fetching member:", e)
        return None
    finally:
        cursor.close()

def list_members(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Member LIMIT %s", (limit,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing members:", e)
        return []
    finally:
        cursor.close()

def update_member(member_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    fields = ", ".join(f"{col} = %s" for col in kwargs)
    values = list(kwargs.values()) + [member_id]
    sql = f"UPDATE Member SET {fields} WHERE member_id = %s"
    try:
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error updating member:", e)
        return False
    finally:
        cursor.close()

def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Member WHERE member_id = %s", (member_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error deleting member:", e)
        return False
    finally:
        cursor.close()

# --- Staff CRUD ---

def add_staff(staff_id, staff_name, staff_role):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT IGNORE INTO Staff (staff_id, staff_name, staff_role) "
           "VALUES (%s, %s, %s)")
    try:
        cursor.execute(sql, (staff_id, staff_name, staff_role))
        conn.commit()
        return True
    except Error as e:
        print("Error adding staff:", e)
        return False
    finally:
        cursor.close()

def get_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Staff WHERE staff_id = %s", (staff_id,))
        return cursor.fetchone()
    except Error as e:
        print("Error fetching staff:", e)
        return None
    finally:
        cursor.close()

def list_staff(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Staff LIMIT %s", (limit,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing staff:", e)
        return []
    finally:
        cursor.close()

def update_staff(staff_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    fields = ", ".join(f"{col} = %s" for col in kwargs)
    values = list(kwargs.values()) + [staff_id]
    sql = f"UPDATE Staff SET {fields} WHERE staff_id = %s"
    try:
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error updating staff:", e)
        return False
    finally:
        cursor.close()

def delete_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Staff WHERE staff_id = %s", (staff_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error deleting staff:", e)
        return False
    finally:
        cursor.close()

# --- Loan CRUD ---

def add_loan(loan_id, member_id, isbn, copy_id, checkout_date, due_date, return_date, overdue_status, staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT IGNORE INTO Loan (loan_id, member_id, isbn, copy_id, checkout_date, due_date, return_date, overdue_status, staff_id) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    try:
        cursor.execute(sql, (loan_id, member_id, isbn, copy_id, checkout_date, due_date, return_date, overdue_status, staff_id))
        conn.commit()
        return True
    except Error as e:
        print("Error adding loan:", e)
        return False
    finally:
        cursor.close()

def get_loan(loan_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Loan WHERE loan_id = %s", (loan_id,))
        return cursor.fetchone()
    except Error as e:
        print("Error fetching loan:", e)
        return None
    finally:
        cursor.close()

def list_loans(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Loan LIMIT %s", (limit,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing loans:", e)
        return []
    finally:
        cursor.close()

def update_loan(loan_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    fields = ", ".join(f"{col} = %s" for col in kwargs)
    values = list(kwargs.values()) + [loan_id]
    sql = f"UPDATE Loan SET {fields} WHERE loan_id = %s"
    try:
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error updating loan:", e)
        return False
    finally:
        cursor.close()

def delete_loan(loan_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Loan WHERE loan_id = %s", (loan_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error deleting loan:", e)
        return False
    finally:
        cursor.close()


# --- Report Queries ---

def list_overdue_loans():
    """
    Returns all rows from the OverdueLoans view.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM OverdueLoans")
        return cursor.fetchall()
    finally:
        cursor.close()


def list_top_borrowers(days=30):
    """
    Returns all rows from the TopBorrowers view.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM TopBorrowers")
        return cursor.fetchall()
    finally:
        cursor.close()


def list_available_copies_by_subject():
    """
    Returns all rows from the AvailableCopiesBySubject view.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM AvailableCopiesBySubject")
        return cursor.fetchall()
    finally:
        cursor.close()


def list_staff_activity(weeks=1):
    """
    Returns all rows from the StaffActivity view.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM StaffActivity")
        return cursor.fetchall()
    finally:
        cursor.close()
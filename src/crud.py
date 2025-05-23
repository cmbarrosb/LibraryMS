import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime, timedelta

# Set to False to prompt for host, user, and database interactively
USE_DEFAULT = True

# --- Table Printing Helper ---
def print_table(rows):
    """Print a list of dicts as a simple table."""
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
    # compute column widths based on display headers and data
    widths = {}
    for h, dh in zip(headers, display_headers):
        max_data = max(len(str(r[h])) for r in rows)
        widths[h] = max(len(dh), max_data)

    # print header
    header_line = " | ".join(dh.ljust(widths[h]) for h, dh in zip(headers, display_headers))
    print(header_line)
    print("-" * len(header_line))
    # print each row
    for r in rows:
        line = " | ".join(str(r[h]).ljust(widths[h]) for h in headers)
        print(line)

# Module-level connection (initialized on first use)
_conn = None

def prompt_credentials():
    """
    Prompt for database connection credentials.
    If USE_DEFAULT is True, use default host/user/db and prompt only for password.
    Otherwise, prompt for all connection info.
    """
    if USE_DEFAULT:
        # Use default host, user, database; prompt only for password
        host = "localhost"
        user = "root"
        database = "library_db"
        password = getpass.getpass("MySQL password for root@localhost: ")
    else:
        # Prompt for all connection details
        host = input("Host [localhost]: ") or "localhost"
        user = input("Username [root]: ") or "root"
        password = getpass.getpass("Password: ")
        database = input("Database [library_db]: ") or "library_db"
    return host, user, password, database

def open_connection(host, user, password, database):
    config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }
    return mysql.connector.connect(**config)

def get_connection():
    """Return the existing database connection."""
    global _conn
    if _conn is None:
        raise RuntimeError("Database connection has not been initialized.")
    return _conn

def add_book(isbn, title, subject, author, description):
    """Insert a new book into the Book table."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO Book (isbn, title, subject, author, description) "
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
    """Fetch a single book by ISBN."""
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

def list_books():
    """List books, prompting the user for how many to return."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Show total number of books
        cursor.execute("SELECT COUNT(*) AS total FROM Book;")
        total = cursor.fetchone()['total']
        print(f"There are {total} books in the database.")
        count = input("How many books would you like to list? [10]: ").strip()
        try:
            n = int(count)
        except ValueError:
            print("Invalid number; defaulting to 10.")
            n = 10
        cursor.execute("SELECT * FROM Book LIMIT %s", (n,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing books:", e)
        return []
    finally:
        cursor.close()

def update_book(isbn, **kwargs):
    """Update book fields given as keyword arguments."""
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
    """Delete a book by ISBN."""
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
    """Insert a new copy into the Copy table."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO Copy (isbn, copy_id, status, location) "
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
    """Fetch a single copy by ISBN and copy_id."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Copy WHERE isbn = %s AND copy_id = %s",
            (isbn, copy_id)
        )
        return cursor.fetchone()
    except Error as e:
        print("Error fetching copy:", e)
        return None
    finally:
        cursor.close()

def list_copies():
    """List copies, prompting the user for how many to return."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Show total number of copies
        cursor.execute("SELECT COUNT(*) AS total FROM Copy;")
        total = cursor.fetchone()['total']
        print(f"There are {total} copies in the database.")
        count = input("How many copies would you like to list? [10]: ").strip()
        try:
            n = int(count)
        except ValueError:
            print("Invalid number; defaulting to 10.")
            n = 10
        cursor.execute("SELECT * FROM Copy LIMIT %s", (n,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing copies:", e)
        return []
    finally:
        cursor.close()

def update_copy(isbn, copy_id, **kwargs):
    """Update copy fields given keyword arguments."""
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
    """Delete a copy by ISBN and copy_id."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Copy WHERE isbn = %s AND copy_id = %s",
            (isbn, copy_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print("Error deleting copy:", e)
        return False
    finally:
        cursor.close()

# --- Member CRUD ---

def add_member(member_id, name, ssn, address, expiration_date, active_flag, professor_privileges):
    """Insert a new member into the Member table."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO Member "
           "(member_id, name, ssn, address, expiration_date, active_flag, professor_privileges) "
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
    """Fetch a single member by member_id."""
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

def list_members():
    """List members, prompting the user for how many to return."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Show total number of members
        cursor.execute("SELECT COUNT(*) AS total FROM Member;")
        total = cursor.fetchone()['total']
        print(f"There are {total} members in the database.")
        count = input("How many members would you like to list? [10]: ").strip()
        try:
            n = int(count)
        except ValueError:
            print("Invalid number; defaulting to 10.")
            n = 10
        cursor.execute("SELECT * FROM Member LIMIT %s", (n,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing members:", e)
        return []
    finally:
        cursor.close()

def update_member(member_id, **kwargs):
    """Update member fields given keyword arguments."""
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
    """Delete a member by member_id."""
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
    """Insert a new staff member into the Staff table."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO Staff (staff_id, staff_name, staff_role) "
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
    """Fetch a single staff member by staff_id."""
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

def list_staff():
    """List staff members, prompting the user for how many to return."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Show total number of staff
        cursor.execute("SELECT COUNT(*) AS total FROM Staff;")
        total = cursor.fetchone()['total']
        print(f"There are {total} staff members in the database.")
        count = input("How many staff members would you like to list? [10]: ").strip()
        try:
            n = int(count)
        except ValueError:
            print("Invalid number; defaulting to 10.")
            n = 10
        cursor.execute("SELECT * FROM Staff LIMIT %s", (n,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing staff:", e)
        return []
    finally:
        cursor.close()

def update_staff(staff_id, **kwargs):
    """Update staff fields given keyword arguments."""
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
    """Delete a staff member by staff_id."""
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
    """Insert a new loan into the Loan table."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO Loan "
           "(loan_id, member_id, isbn, copy_id, checkout_date, due_date, return_date, overdue_status, staff_id) "
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
    """Fetch a single loan by loan_id."""
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

def list_loans():
    """List loans, prompting the user for how many to return."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Show total number of loans
        cursor.execute("SELECT COUNT(*) AS total FROM Loan;")
        total = cursor.fetchone()['total']
        print(f"There are {total} loans in the database.")
        count = input("How many loans would you like to list? [10]: ").strip()
        try:
            n = int(count)
        except ValueError:
            print("Invalid number; defaulting to 10.")
            n = 10
        cursor.execute("SELECT * FROM Loan LIMIT %s", (n,))
        return cursor.fetchall()
    except Error as e:
        print("Error listing loans:", e)
        return []
    finally:
        cursor.close()

def update_loan(loan_id, **kwargs):
    """Update loan fields given keyword arguments."""
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
    """Delete a loan by loan_id."""
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

def loans_menu():
    """Submenu for Loan operations."""
    while True:
        print("\nLoans ▶")
        print(" 1. Add Loan")
        print(" 2. Get Loan")
        print(" 3. List Loans")
        print(" 4. Update Loan")
        print(" 5. Delete Loan")
        print(" 0. Back")
        choice = input("Loan choice: ").strip()
        if choice == "1":
            # Prompt for Loan ID
            lid = int(input("Loan ID: "))

            # Validate Member ID
            while True:
                mid = int(input("Member ID (0 to abort): "))
                if mid == 0:
                    print("Aborting add loan.")
                    break
                member = get_member(mid)
                if member is None:
                    print("Member ID not found. Please try again or enter 0 to abort.")
                    continue
                break
            if mid == 0:
                continue

            # Determine default due date based on member privileges
            days = 90 if member.get('professor_privileges') else 30

            # Validate Copy (ISBN + Copy ID)
            while True:
                isbn = input("ISBN (or 0 to abort): ").strip()
                if isbn == "0":
                    print("Aborting add loan.")
                    break
                try:
                    cid = int(input("Copy ID: "))
                except ValueError:
                    print("Invalid Copy ID; please enter an integer.")
                    continue
                copy_rec = get_copy(isbn, cid)
                if copy_rec is None:
                    print("Copy not found. Please try again or enter 0 to abort.")
                    continue
                break
            if isbn == "0":
                continue

            # Prompt for Checkout Date with default today
            default_co = datetime.today().date().isoformat()
            co = input(f"Checkout Date (YYYY-MM-DD) [Today]: ").strip() or default_co

            # Compute and prompt for Due Date with default based on privileges
            default_due = (datetime.strptime(co, "%Y-%m-%d") + timedelta(days=days)).date().isoformat()
            du = input(f"Due Date (YYYY-MM-DD) [{days} days]: ").strip() or default_due

            # Prompt for Return Date with default None
            re = input("Return Date (YYYY-MM-DD) [None]: ").strip() or None

            # Prompt for Overdue Status with default None
            ans = input("Overdue Status ([N]one, Notice[S]ent, [L]ate) [None]: ").strip()
            if ans == "N" or "n":
                status = "None"
            elif ans == "S" or "s":
                status = "Notice Sent"
            elif ans == "L" or "l":
                status = "Late"
            else:
                print("Defaulting to None.")
                status = "None"
            # Validate Staff ID
            while True:
                try:
                    sid = int(input("Staff ID (0 to abort): "))
                except ValueError:
                    print("Invalid Staff ID; please enter an integer.")
                    continue
                if sid == 0:
                    print("Aborting add loan.")
                    break
                staff_rec = get_staff(sid)
                if staff_rec is None:
                    print("Staff ID not found. Please try again or enter 0 to abort.")
                    continue
                break
            if sid == 0:
                continue

            # Finally, add the loan
            print("Added Loan:", add_loan(lid, mid, isbn, cid, co, du, re, status, sid))
        elif choice == "2":
            lid = int(input("Loan ID: "))
            rec = get_loan(lid)
            if rec:
                print_table([rec])
            else:
                print("No loan found.")
        elif choice == "3":
            rows = list_loans()
            print_table(rows)
        elif choice == "4":
            lid = int(input("Loan ID: "))
            field = input("Field to update: ")
            value = input("New value: ")
            print("Updated Loan:", update_loan(lid, **{field: value}))
        elif choice == "5":
            lid = int(input("Loan ID: "))
            print("Deleted Loan:", delete_loan(lid))
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")



def books_menu():
    """Submenu for Book operations."""
    while True:
        print("\nBooks ▶")
        print(" 1. Add Book")
        print(" 2. Get Book")
        print(" 3. List Books")
        print(" 4. Update Book")
        print(" 5. Delete Book")
        print(" 0. Back")
        choice = input("Book choice: ").strip()
        if choice == "1":
            isbn = input("ISBN: ")
            title = input("Title: ")
            subject = input("Subject: ")
            author = input("Author: ")
            description = input("Description: ")
            print("Added Book:", add_book(isbn, title, subject, author, description))
        elif choice == "2":
            isbn = input("ISBN: ")
            rec = get_book(isbn)
            if rec:
                print_table([rec])
            else:
                print("No book found.")
        elif choice == "3":
            rows = list_books()
            print_table(rows)
        elif choice == "4":
            isbn = input("ISBN: ")
            field = input("Field to update: ")
            value = input("New value: ")
            print("Updated Book:", update_book(isbn, **{field: value}))
        elif choice == "5":
            isbn = input("ISBN: ")
            print("Deleted Book:", delete_book(isbn))
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def copies_menu():
    """Submenu for Copy operations."""
    while True:
        print("\nCopies ▶")
        print(" 1. Add Copy")
        print(" 2. Get Copy")
        print(" 3. List Copies")
        print(" 4. Update Copy")
        print(" 5. Delete Copy")
        print(" 0. Back")
        choice = input("Copy choice: ").strip()
        if choice == "1":
            isbn = input("ISBN: ")
            cid = int(input("Copy ID: "))
            status = input("Status: ")
            location = input("Location: ")
            print("Added Copy:", add_copy(isbn, cid, status, location))
        elif choice == "2":
            isbn = input("ISBN: ")
            cid = int(input("Copy ID: "))
            rec = get_copy(isbn, cid)
            if rec:
                print_table([rec])
            else:
                print("No copy found.")
        elif choice == "3":
            rows = list_copies()
            print_table(rows)
        elif choice == "4":
            isbn = input("ISBN: ")
            cid = int(input("Copy ID: "))
            field = input("Field to update: ")
            value = input("New value: ")
            print("Updated Copy:", update_copy(isbn, cid, **{field: value}))
        elif choice == "5":
            isbn = input("ISBN: ")
            cid = int(input("Copy ID: "))
            print("Deleted Copy:", delete_copy(isbn, cid))
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def members_menu():
    """Submenu for Member operations."""
    while True:
        print("\nMembers ▶")
        print(" 1. Add Member")
        print(" 2. Get Member")
        print(" 3. List Members")
        print(" 4. Update Member")
        print(" 5. Delete Member")
        print(" 0. Back")
        choice = input("Member choice: ").strip()
        if choice == "1":
            mid = int(input("Member ID: "))
            name = input("Name: ")
            ssn = input("SSN: ")
            addr = input("Address: ")
            exp = input("Expiration Date (YYYY-MM-DD): ")
            active = int(input("Active (1 or 0): "))
            prof = int(input("Professor Privileges (1 or 0): "))
            print("Added Member:", add_member(mid, name, ssn, addr, exp, active, prof))
        elif choice == "2":
            mid = int(input("Member ID: "))
            rec = get_member(mid)
            if rec:
                print_table([rec])
            else:
                print("No member found.")
        elif choice == "3":
            rows = list_members()
            print_table(rows)
        elif choice == "4":
            mid = int(input("Member ID: "))
            field = input("Field to update: ")
            value = input("New value: ")
            print("Updated Member:", update_member(mid, **{field: value}))
        elif choice == "5":
            mid = int(input("Member ID: "))
            print("Deleted Member:", delete_member(mid))
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def staff_menu():
    """Submenu for Staff operations."""
    while True:
        print("\nStaff ▶")
        print(" 1. Add Staff")
        print(" 2. Get Staff")
        print(" 3. List Staff")
        print(" 4. Update Staff")
        print(" 5. Delete Staff")
        print(" 0. Back")
        choice = input("Staff choice: ").strip()
        if choice == "1":
            sid = int(input("Staff ID: "))
            name = input("Staff Name: ")
            role = input("Staff Role: ")
            print("Added Staff:", add_staff(sid, name, role))
        elif choice == "2":
            sid = int(input("Staff ID: "))
            rec = get_staff(sid)
            if rec:
                print_table([rec])
            else:
                print("No staff found.")
        elif choice == "3":
            rows = list_staff()
            print_table(rows)
        elif choice == "4":
            sid = int(input("Staff ID: "))
            field = input("Field to update: ")
            value = input("New value: ")
            print("Updated Staff:", update_staff(sid, **{field: value}))
        elif choice == "5":
            sid = int(input("Staff ID: "))
            print("Deleted Staff:", delete_staff(sid))
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def main():
    """Main menu to select an entity subsystem."""
    global _conn
    # Prompt for password and open connection once
    host, user, password, database = prompt_credentials()
    _conn = open_connection(host, user, password, database)
    while True:
        print("\nLibraryMS Main Menu:")
        print("1) Books")
        print("2) Copies")
        print("3) Members")
        print("4) Staff")
        print("5) Loans")
        print("0) Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            books_menu()
        elif choice == "2":
            copies_menu()
        elif choice == "3":
            members_menu()
        elif choice == "4":
            staff_menu()
        elif choice == "5":
            loans_menu()
        elif choice == "0":
            print("Goodbye!")
            if _conn:
                _conn.close()
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
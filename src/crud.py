import mysql.connector
from mysql.connector import Error
import getpass

# Module-level connection (initialized on first use)
_conn = None

def prompt_credentials():
    """Prompt only for the database password; use default host, user, database."""
    host = "localhost"
    user = "root"
    database = "library_db"
    password = getpass.getpass("MySQL password for root@localhost: ")
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
        count = input("How many books would you like to list? ")
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
        count = input("How many copies would you like to list? ")
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
        count = input("How many members would you like to list? ")
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
        count = input("How many staff members would you like to list? ")
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
            print("Book:", get_book(isbn))
        elif choice == "3":
            print("Books:", list_books())
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
            print("Copy:", get_copy(isbn, cid))
        elif choice == "3":
            print("Copies:", list_copies())
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
            print("Member:", get_member(mid))
        elif choice == "3":
            print("Members:", list_members())
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
            print("Staff:", get_staff(sid))
        elif choice == "3":
            print("Staff Members:", list_staff())
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
        elif choice == "0":
            print("Goodbye!")
            if _conn:
                _conn.close()
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
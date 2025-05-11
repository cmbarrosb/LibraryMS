import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime, timedelta
import init_db

from crud_lib import (
    prompt_credentials,
    open_connection,
    get_connection,
    print_table,
    list_overdue_loans,
    list_top_borrowers,
    list_available_copies_by_subject,
    list_staff_activity,
)

from crud_lib import (
    add_book, add_copy, add_member, add_staff, add_loan,
    get_book, get_copy, get_member, get_staff, get_loan,
    list_books, list_copies, list_members, list_staff, list_loans,
    update_book, update_copy, update_member, update_staff, update_loan,
    delete_book, delete_copy, delete_member, delete_staff, delete_loan
)
# --- DELETE MENU ---
def delete_menu():
    """Submenu for deleting records."""
    while True:
        print("\nDelete Record ▶")
        print(" 1) Book")
        print(" 2) Copy")
        print(" 3) Member")
        print(" 4) Staff")
        print(" 5) Loan")
        print(" 0) Back")
        choice = input("Select type to delete: ").strip()
        if choice == "1":
            isbn = input("ISBN: ")
            success = delete_book(isbn)
            print("Book deleted successfully." if success else "Failed to delete book.")
        elif choice == "2":
            isbn = input("ISBN: ")
            cid = int(input("Copy ID: "))
            success = delete_copy(isbn, cid)
            print("Copy deleted successfully." if success else "Failed to delete copy.")
        elif choice == "3":
            mid = int(input("Member ID: "))
            success = delete_member(mid)
            print("Member deleted successfully." if success else "Failed to delete member.")
        elif choice == "4":
            sid = int(input("Staff ID: "))
            success = delete_staff(sid)
            print("Staff deleted successfully." if success else "Failed to delete staff.")
        elif choice == "5":
            lid = int(input("Loan ID: "))
            success = delete_loan(lid)
            print("Loan deleted successfully." if success else "Failed to delete loan.")
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

_conn = None

def add_record_menu():
    """Submenu for Add Record operations."""
    while True:
        print("\nAdd Record ▶")
        print(" 1) Book")
        print(" 2) Copy")
        print(" 3) Member")
        print(" 4) Staff")
        print(" 5) Loan")
        print(" 0) Back")
        choice = input("Select type to add: ").strip()

        if choice == "1":
            isbn = input("ISBN: ")
            title = input("Title: ")
            subject = input("Subject: ")
            author = input("Author: ")
            description = input("Description: ")
            success = add_book(isbn, title, subject, author, description)
            print("Book added successfully." if success else "Failed to add book.")
        elif choice == "2":
            isbn = input("ISBN: ")
            # validate Copy ID
            while True:
                try:
                    cid = int(input("Copy ID: "))
                    break
                except ValueError:
                    print("Invalid Copy ID; please enter an integer.")
            status = input("Status (Available/Not Available): ")
            location = input("Location: ")
            success = add_copy(isbn, cid, status, location)
            print("Copy added successfully." if success else "Failed to add copy.")
        elif choice == "3":
            while True:
                try:
                    mid = int(input("Member ID: "))
                    break
                except ValueError:
                    print("Invalid Member ID; please enter an integer.")
            name = input("Name: ")
            ssn = input("SSN: ")
            address = input("Address: ")
            # default expiration one year from today
            default_exp = (datetime.today().date() + timedelta(days=365)).isoformat()
            print(f"Expiration Date set to {default_exp}")
            active_flag = 1
            prof = input("Professor Privileges (1 or 0) [0]: ").strip() or "0"
            success = add_member(mid, name, ssn, address, default_exp, active_flag, int(prof))
            print("Member added successfully." if success else "Failed to add member.")
        elif choice == "4":
            while True:
                try:
                    sid = int(input("Staff ID: "))
                    break
                except ValueError:
                    print("Invalid Staff ID; please enter an integer.")
            sname = input("Staff Name: ")
            role = input("Staff Role: ")
            success = add_staff(sid, sname, role)
            print("Staff added successfully." if success else "Failed to add staff.")
        elif choice == "5":
            # Add Loan logic from loans_menu
            while True:
                try:
                    loan_id = int(input("Loan ID: "))
                    break
                except ValueError:
                    print("Invalid Loan ID; please enter an integer.")
            # Validate Member ID exists
            try:
                member_id = int(input("Member ID: "))
            except ValueError:
                print("Invalid Member ID; aborting.")
                return
            member_row = None
            for m in list_members():
                if m["member_id"] == member_id:
                    member_row = m
                    break
            if not member_row:
                print("Member ID does not exist; aborting.")
                return
            # Determine default days
            prof = member_row.get("professor_privileges", 0)
            default_days = 90 if prof else 30
            # Validate ISBN and Copy ID exist
            isbn = input("ISBN: ")
            copy_id = None
            try:
                copy_id = int(input("Copy ID: "))
            except ValueError:
                print("Invalid Copy ID; aborting.")
                return
            copy_row = None
            for c in list_copies():
                if c["isbn"] == isbn and c["copy_id"] == copy_id:
                    copy_row = c
                    break
            if not copy_row:
                print("Copy (ISBN + Copy ID) does not exist; aborting.")
                return
            # Prompt Checkout Date with default today
            today_str = datetime.today().date().isoformat()
            checkout_date = input(f"Checkout Date [{today_str}]: ").strip() or today_str
            # Compute and prompt Due Date with default days ahead
            try:
                due_default = (datetime.fromisoformat(checkout_date).date() + timedelta(days=default_days)).isoformat()
            except Exception:
                due_default = (datetime.today().date() + timedelta(days=default_days)).isoformat()
            due_date = input(f"Due Date [{due_default}]: ").strip() or due_default
            # Prompt Return Date default None
            return_date = input("Return Date [None]: ").strip() or None
            # Prompt Overdue Status default None
            overdue_status = input("Overdue Status [None]: ").strip() or None
            # Validate Staff ID exists
            try:
                staff_id = int(input("Staff ID: "))
            except ValueError:
                print("Invalid Staff ID; aborting.")
                return
            staff_row = None
            for s in list_staff():
                if s["staff_id"] == staff_id:
                    staff_row = s
                    break
            if not staff_row:
                print("Staff ID does not exist; aborting.")
                return
            success = add_loan(loan_id, member_id, isbn, copy_id, checkout_date, due_date, return_date, overdue_status, staff_id)
            print("Loan added successfully." if success else "Failed to add loan.")
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def get_menu():
    """Submenu for fetching or listing records."""
    while True:
        print("\nSearch/List Records ▶")
        print(" 1) Search specific record")
        print(" 2) List Books")
        print(" 3) List Copies")
        print(" 4) List Members")
        print(" 5) List Staff")
        print(" 6) List Loans")
        print(" 0) Back")
        choice = input("Select option: ").strip()

        if choice == "1":
            # Two-step entity search
            print("Search ▶")
            print(" 1) Book by ISBN")
            print(" 2) Copy by ISBN and Copy ID")
            print(" 3) Member by Member ID")
            print(" 4) Staff by Staff ID")
            print(" 5) Loan by Loan ID")
            sub = input("Select entity to search: ").strip()
            if sub == "1":
                isbn = input("ISBN: ")
                rec = get_book(isbn)
            elif sub == "2":
                isbn = input("ISBN: ")
                cid = int(input("Copy ID: "))
                rec = get_copy(isbn, cid)
            elif sub == "3":
                mid = int(input("Member ID: "))
                rec = get_member(mid)
            elif sub == "4":
                sid = int(input("Staff ID: "))
                rec = get_staff(sid)
            elif sub == "5":
                lid = int(input("Loan ID: "))
                rec = get_loan(lid)
            else:
                print("Invalid choice.")
                continue
            # Display result
            if rec:
                print_table([rec])
            else:
                print("No record found.")
        elif choice == "2":
            rows = list_books()
            print_table(rows)
        elif choice == "3":
            rows = list_copies()
            print_table(rows)
        elif choice == "4":
            rows = list_members()
            print_table(rows)
        elif choice == "5":
            rows = list_staff()
            print_table(rows)
        elif choice == "6":
            rows = list_loans()
            print_table(rows)
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def update_menu():
    """Submenu for Update operations (delete options removed)."""
    while True:
        print("\nUpdate Record ▶")
        print(" 1) Update Book")
        print(" 2) Update Copy")
        print(" 3) Update Member")
        print(" 4) Update Staff")
        print(" 5) Update Loan")
        print(" 0) Back")
        choice = input("Select option: ").strip()

        if choice == "1":
            # Update Book
            isbn = input("ISBN: ")
            confirm = input("Are you sure you want to update this record? (y/N): ").strip().lower()
            if confirm != "y":
                print("Update cancelled.")
                continue
            field = input("Field to update: ")
            value = input("New value: ")
            success = update_book(isbn, **{field: value})
            print("Book updated successfully." if success else "Failed to update book.")
        elif choice == "2":
            # Update Copy
            isbn = input("ISBN: ")
            cid = int(input("Copy ID: "))
            confirm = input("Are you sure you want to update this record? (y/N): ").strip().lower()
            if confirm != "y":
                print("Update cancelled.")
                continue
            field = input("Field to update: ")
            value = input("New value: ")
            success = update_copy(isbn, cid, **{field: value})
            print("Copy updated successfully." if success else "Failed to update copy.")
        elif choice == "3":
            # Update Member
            mid = int(input("Member ID: "))
            confirm = input("Are you sure you want to update this record? (y/N): ").strip().lower()
            if confirm != "y":
                print("Update cancelled.")
                continue
            field = input("Field to update: ")
            value = input("New value: ")
            success = update_member(mid, **{field: value})
            print("Member updated successfully." if success else "Failed to update member.")
        elif choice == "4":
            # Update Staff
            sid = int(input("Staff ID: "))
            confirm = input("Are you sure you want to update this record? (y/N): ").strip().lower()
            if confirm != "y":
                print("Update cancelled.")
                continue
            field = input("Field to update: ")
            value = input("New value: ")
            success = update_staff(sid, **{field: value})
            print("Staff updated successfully." if success else "Failed to update staff.")
        elif choice == "5":
            # Update Loan
            lid = int(input("Loan ID: "))
            confirm = input("Are you sure you want to update this record? (y/N): ").strip().lower()
            if confirm != "y":
                print("Update cancelled.")
                continue
            field = input("Field to update: ")
            value = input("New value: ")
            success = update_loan(lid, **{field: value})
            print("Loan updated successfully." if success else "Failed to update loan.")
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def reports_menu():
    """Submenu for library reports."""
    while True:
        print("\nReports ▶")
        print(" 1) Overdue Loans")
        print(" 2) Top Borrowers (last 30 days)")
        print(" 3) Available Copies by Subject")
        print(" 4) Staff Activity (check-outs per week)")
        print(" 0) Back")
        choice = input("Select report: ").strip()
        if choice == "1":
            rows = list_overdue_loans()
            print_table(rows)
        elif choice == "2":
            days = input("Look back how many days? [30]: ").strip() or "30"
            try:
                d = int(days)
            except ValueError:
                print("Invalid input; defaulting to 30 days.")
                d = 30
            rows = list_top_borrowers(d)
            print_table(rows)
        elif choice == "3":
            rows = list_available_copies_by_subject()
            print_table(rows)
        elif choice == "4":
            weeks = input("Look back how many weeks? [1]: ").strip() or "1"
            try:
                w = int(weeks)
            except ValueError:
                print("Invalid input; defaulting to 1 week.")
                w = 1
            rows = list_staff_activity(w)
            print_table(rows)
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def main():
    """Top‐level action menu: Add, Get, or Update (0 to exit)."""
    global _conn
    host, user, password, database = prompt_credentials()
    _conn = open_connection(host, user, password, database)

    while True:
        print("\nWelcome to the Library Management System! What would you like to do today?")
        print("1) Add Record")
        print("2) Get Record")
        print("3) Update Record")
        print("4) Delete Record")
        print("5) Initialize Database")
        print("6) Reports")
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
        elif choice == "4":
            delete_menu()
        elif choice == "5":
            print("Initializing database schema and data...")
            init_db.main()
            print("Database initialization complete.")
        elif choice == "6":
            reports_menu()
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()

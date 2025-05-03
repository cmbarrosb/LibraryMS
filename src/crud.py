

import mysql.connector
from mysql.connector import Error

def get_connection():
    """Open a new database connection."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password_here',
        database='library_db'
    )

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
        conn.close()

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
        conn.close()

def list_books(limit=10):
    """List up to `limit` books."""
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
        conn.close()

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
        conn.close()

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
        conn.close()

if __name__ == '__main__':
    # Quick smoke tests for Book CRUD
    print("Adding sample book:", add_book('0001', 'Test Book', 'Testing', 'Tester', 'A test book.'))
    print("Fetching sample book:", get_book('0001'))
    print("Listing books:", list_books(5))
    print("Updating sample book:", update_book('0001', title='Updated Test Book'))
    print("Fetching updated book:", get_book('0001'))
    print("Deleting sample book:", delete_book('0001'))
    print("Fetching deleted book (should be None):", get_book('0001'))
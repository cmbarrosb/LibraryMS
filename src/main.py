cursor = _conn.cursor(dictionary=True)
cursor.execute("""
SELECT B.isbn, B.title, C.copy_id, C.status
FROM Book B
JOIN Copy C ON B.isbn = C.isbn
WHERE C.status = 'Available';
""")
rows = cursor.fetchall()
for row in rows:
    print(row)
Python 3.12.6 (v3.12.6:a4a2d2b0d85, Sep  6 2024, 16:08:03) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.

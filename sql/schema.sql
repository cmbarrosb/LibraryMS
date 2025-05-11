-- Create database and use it
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Book Table
CREATE TABLE IF NOT EXISTS Book (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(100),
    subject VARCHAR(50),
    author VARCHAR(100),
    description TEXT
);

-- Copy Table
CREATE TABLE IF NOT EXISTS Copy (
    isbn VARCHAR(20),
    copy_id INT,
    status ENUM('Available','Not Available'),
    location VARCHAR(100),
    PRIMARY KEY (isbn, copy_id),
    FOREIGN KEY (isbn) REFERENCES Book(isbn)
);

-- Member Table
CREATE TABLE IF NOT EXISTS Member (
    member_id INT PRIMARY KEY,
    name VARCHAR(100),
    ssn CHAR(9),
    address VARCHAR(200),
    expiration_date DATE,
    active_flag BOOLEAN,
    professor_privileges BOOLEAN
);

-- Staff Table
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT PRIMARY KEY,
    staff_name VARCHAR(100),
    staff_role VARCHAR(50)
);

-- Loan Table
CREATE TABLE IF NOT EXISTS Loan (
    loan_id INT PRIMARY KEY,
    member_id INT,
    isbn VARCHAR(20),
    copy_id INT,
    checkout_date DATE,
    due_date DATE,
    return_date DATE,
    overdue_status ENUM('None','NoticeSent','Late'),
    staff_id INT,
    FOREIGN KEY (member_id) REFERENCES Member(member_id),
    FOREIGN KEY (isbn, copy_id) REFERENCES Copy(isbn, copy_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- Overdue Loans View
CREATE OR REPLACE VIEW OverdueLoans AS
SELECT
    L.loan_id      AS loan_id,
    M.name         AS member_name,
    B.title        AS book_title,
    L.due_date     AS due_date,
    DATEDIFF(CURDATE(), L.due_date) AS days_overdue,
    S.staff_name   AS processed_by
FROM Loan L
JOIN Member M  ON L.member_id = M.member_id
JOIN Book   B  ON L.isbn      = B.isbn
JOIN Staff  S  ON L.staff_id  = S.staff_id
WHERE L.overdue_status = 'Late'
  AND L.return_date IS NULL;

-- Top Borrowers (last 30 days)
CREATE OR REPLACE VIEW TopBorrowers AS
SELECT
    M.member_id    AS member_id,
    M.name         AS member_name,
    COUNT(*)       AS loans_count
FROM Loan L
JOIN Member M ON L.member_id = M.member_id
WHERE L.checkout_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY M.member_id, M.name
ORDER BY loans_count DESC;

-- Available Copies by Subject
CREATE OR REPLACE VIEW AvailableCopiesBySubject AS
SELECT
    B.subject AS subject,
    COUNT(*)  AS available_copies
FROM Copy C
JOIN Book B ON C.isbn = B.isbn
WHERE C.status = 'Available'
GROUP BY B.subject;

-- Staff Activity (last week)
CREATE OR REPLACE VIEW StaffActivity AS
SELECT
    S.staff_id,
    S.staff_name,
    COUNT(*) AS processed_loans
FROM Loan L
JOIN Staff S ON L.staff_id = S.staff_id
WHERE L.checkout_date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK)
GROUP BY S.staff_id, S.staff_name
ORDER BY processed_loans DESC;

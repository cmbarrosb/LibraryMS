-- Book Table
CREATE TABLE IF NOT EXISTS Book (
    isbn VARCHAR(20) PRIMARY KEY,            -- ISBN
    title VARCHAR(100),                      -- Title
    subject VARCHAR(50),                     -- Subject
    author VARCHAR(100),                     -- Author
    description TEXT                         -- Description
);

-- Copy Table
CREATE TABLE IF NOT EXISTS Copy (
    isbn VARCHAR(20),                        -- ISBN (FK)
    copy_id INT,                             -- CopyID
    status ENUM('Available','Not Available'),-- Copy status
    location VARCHAR(100),                   -- Location
    PRIMARY KEY (isbn, copy_id),
    FOREIGN KEY (isbn) REFERENCES Book(isbn)
);

-- Member Table
CREATE TABLE IF NOT EXISTS Member (
    member_id INT PRIMARY KEY,               -- MemberID
    name VARCHAR(100),                       -- Name
    ssn CHAR(9),                             -- SSN
    address VARCHAR(200),                    -- Address
    expiration_date DATE,                    -- Expiration date
    active_flag BOOLEAN,                     -- Active membership flag
    professor_privileges BOOLEAN             -- Professor privileges
);

-- Staff Table
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT PRIMARY KEY,                -- StaffID
    staff_name VARCHAR(100),                 -- Staff name
    staff_role VARCHAR(50)                   -- Staff role
);

-- Loan Table
CREATE TABLE IF NOT EXISTS Loan (
    loan_id INT PRIMARY KEY,                 -- LoanID
    member_id INT,                           -- MemberID (FK)
    isbn VARCHAR(20),                        -- ISBN (FK)
    copy_id INT,                             -- CopyID (FK)
    checkout_date DATE,                      -- Checkout date
    due_date DATE,                           -- Due date
    return_date DATE,                        -- Return date
    overdue_status ENUM('None','NoticeSent','Late'), -- Overdue status
    staff_id INT,                            -- StaffID (FK)
    FOREIGN KEY (member_id) REFERENCES Member(member_id),
    FOREIGN KEY (isbn, copy_id) REFERENCES Copy(isbn, copy_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

--overdue Table
-- View for Overdue Loans Report
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

-- View for Top Borrowers (last 30 days)
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

-- View for Available Copies by Subject
CREATE OR REPLACE VIEW AvailableCopiesBySubject AS
SELECT
B.subject               AS subject,
COUNT(*)               AS available_copies
FROM Copy C
JOIN Book B ON C.isbn = B.isbn
WHERE C.status = ‘Available’
GROUP BY B.subject;

-- View for Staff Activity (check-outs per week)
CREATE OR REPLACE VIEW StaffActivity AS
SELECT
S.staff_id             AS staff_id,
S.staff_name           AS staff_name,
COUNT(*)               AS processed_loans
FROM Loan L
JOIN Staff S ON L.staff_id = S.staff_id
WHERE L.checkout_date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK)
GROUP BY S.staff_id, S.staff_name
ORDER BY processed_loans DESC;
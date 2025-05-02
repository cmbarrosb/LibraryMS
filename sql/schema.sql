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
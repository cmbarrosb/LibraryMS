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
    status ENUM('Available', 'Not Available'),
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

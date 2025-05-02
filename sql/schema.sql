-- Book Table
CREATE TABLE IF NOT EXISTS Book (
    I VARCHAR(20) PRIMARY KEY,            -- ISBN
    T VARCHAR(100),                       -- Title
    S VARCHAR(50),                        -- Subject
    A VARCHAR(100),                       -- Author
    D TEXT                                -- Description
);

-- Copy Table
CREATE TABLE IF NOT EXISTS Copy (
    I VARCHAR(20),                        -- ISBN (FK)
    C INT,                                -- CopyID
    V ENUM('Available', 'Not Available'),-- Copy Status
    L VARCHAR(100),                       -- Location
    PRIMARY KEY (I, C),
    FOREIGN KEY (I) REFERENCES Book(I)
);

-- Member Table
CREATE TABLE IF NOT EXISTS Member (
    M INT PRIMARY KEY,                    -- MemberID
    N VARCHAR(100),                       -- Name
    Q CHAR(9),                            -- SSN
    X VARCHAR(200),                       -- Address
    E DATE,                               -- Expiration Date
    Z BOOLEAN                             -- Active Membership
    P BOOLEAN                             -- Professor privileges (longer loan/grace periods)
);

-- Staff Table
CREATE TABLE IF NOT EXISTS Staff (
    H INT PRIMARY KEY,                    -- StaffID
    Z1 VARCHAR(100),                      -- Staff Name
    Z2 VARCHAR(50)                        -- Role
);

-- Loan Table
CREATE TABLE IF NOT EXISTS Loan (
    O INT PRIMARY KEY,                    -- LoanID
    M INT,                                -- MemberID (FK)
    I VARCHAR(20),                        -- ISBN (FK)
    C INT,                                -- CopyID (FK w/ ISBN)
    B DATE,                               -- Checkout Date
    U DATE,                               -- Due Date
    W DATE,                               -- Return Date
    K ENUM('None', 'NoticeSent', 'Late'),-- Overdue Status
    H INT,                                -- StaffID (FK)
    FOREIGN KEY (M) REFERENCES Member(M),
    FOREIGN KEY (I, C) REFERENCES Copy(I, C),
    FOREIGN KEY (H) REFERENCES Staff(H)
);

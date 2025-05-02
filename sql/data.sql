-- Book data
INSERT INTO Book (I, T, S, A, D) VALUES
('9780131101630', 'The C Programming Language', 'Computer Science', 'Kernighan & Ritchie', 'Classic intro to C.'),
('9780262033848', 'Introduction to Algorithms', 'Algorithms', 'Cormen et al.', 'Comprehensive guide to algorithms.');

-- Copy data
INSERT INTO Copy (I, C, V, L) VALUES
('9780131101630', 1, 'Available', 'Shelf A1'),
('9780131101630', 2, 'Not Available', 'Shelf A1'),
('9780262033848', 1, 'Available', 'Shelf B2');

-- Member data
INSERT INTO Member (M, N, Q, X, Y, E, Z) VALUES
(1001, 'Alice Smith', '123456789', '123 Main St', 'North Campus', '2025-12-31', TRUE),
(1002, 'Bob Johnson', '987654321', '456 Oak Ave', 'South Campus', '2024-11-30', TRUE);

-- Staff data
INSERT INTO Staff (H, Z1, Z2) VALUES
(201, 'Linda Wong', 'Librarian'),
(202, 'James Liu', 'Assistant');

-- Loan data
INSERT INTO Loan (O, M, I, C, B, U, W, F, K, J, H) VALUES
(1, 1001, '9780131101630', 2, '2025-04-01', '2025-04-15', '2025-04-10', 'N/A', 'None', 'N/A', 201),
(2, 1002, '9780262033848', 1, '2025-04-20', '2025-05-04', NULL, 'N/A', 'NoticeSent', 'Reminder sent via email', 202);

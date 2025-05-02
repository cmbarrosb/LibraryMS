-- Book data
INSERT INTO Book (I, T, S, A, D) VALUES
('9780131101630', 'The C Programming Language', 'Computer Science', 'Kernighan & Ritchie', 'Classic intro to C.'),
('9780262033848', 'Introduction to Algorithms', 'Algorithms', 'Cormen et al.', 'Comprehensive guide to algorithms.'),
('9780596009205', 'Head First Java', 'Programming', 'Kathy Sierra', 'Java for beginners, visual approach.'),
('9781492078005', 'Fluent Python', 'Python', 'Luciano Ramalho', 'Advanced Python techniques and tricks.'),
('9780201633610', 'Design Patterns', 'Software Engineering', 'Gamma et al.', 'Classic book on software design patterns.');

-- Copy data
INSERT INTO Copy (I, C, V, L) VALUES
('9780131101630', 1, 'Available', 'Shelf A1'),
('9780131101630', 2, 'Not Available', 'Shelf A1'),
('9780262033848', 1, 'Available', 'Shelf B2'),
('9780596009205', 1, 'Available', 'Shelf C1'),
('9781492078005', 1, 'Not Available', 'Shelf C2');

-- Member data
INSERT INTO Member (M, N, Q, X, Y, E, Z) VALUES
(1001, 'Alice Smith', '123456789', '123 Main St', 'North Campus', '2025-12-31', TRUE),
(1002, 'Bob Johnson', '987654321', '456 Oak Ave', 'South Campus', '2024-11-30', TRUE),
(1003, 'Chloe Tran', '111222333', '789 Pine Rd', 'East Campus', '2025-06-15', TRUE),
(1004, 'Daniel Kim', '444555666', '321 Cedar Blvd', 'West Campus', '2025-03-31', FALSE),
(1005, 'Emily Zhang', '777888999', '654 Birch Ln', 'North Campus', '2025-09-20', TRUE);

-- Staff data
INSERT INTO Staff (H, Z1, Z2) VALUES
(201, 'Linda Wong', 'Librarian'),
(202, 'James Liu', 'Assistant'),
(203, 'Mark Rivera', 'Supervisor'),
(204, 'Nina Patel', 'Librarian'),
(205, 'Sara Ochoa', 'Clerk');

-- Loan data
INSERT INTO Loan (O, M, I, C, B, U, W, F, K, J, H) VALUES
(1, 1001, '9780131101630', 2, '2025-04-01', '2025-04-15', '2025-04-10', 'N/A', 'None', 'N/A', 201),
(2, 1002, '9780262033848', 1, '2025-04-20', '2025-05-04', NULL, 'N/A', 'NoticeSent', 'Reminder sent via email', 202),
(3, 1003, '9780596009205', 1, '2025-03-15', '2025-03-29', '2025-04-01', 'Late return', 'Late', 'Overdue by 3 days', 203),
(4, 1004, '9781492078005', 1, '2025-01-10', '2025-01-24', '2025-01-24', 'On time', 'None', '', 204),
(5, 1005, '9780201633610', 1, '2025-04-25', '2025-05-09', NULL, '', 'None', '', 205);

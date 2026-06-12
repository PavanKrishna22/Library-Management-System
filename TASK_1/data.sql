-- LIBRARY MANAGEMENT SYSTEM (LMS) Assessment-1, Phase-1   

 

 -- LIBRARIES  

INSERT INTO Library (name, campus_location, contact_email, phone_number)  

VALUES  

('Library 1', 'Block A', 'lib1@gmail.com', '9000000001'),  

('Library 2', 'Block B', 'lib2@gmail.com', '9000000002'),  

('Library 3', 'Block C', 'lib3@gmail.com', '9000000003');  

 

-- AUTHORS  

INSERT INTO Author (first_name, last_name, birth_date, nationality, biography)  

VALUES  

('Pavan', 'A', '1970-01-01', 'Indian', 'Author 1'),  

('Krishna', 'B', '1975-02-02', 'Indian', 'Author 2'),  

('Steve', 'C', '1980-03-03', 'American', 'Author 3'),  

('Vighnesh', 'D', '1985-04-04', 'Indian ', 'Author 4'),  

('David', 'E', '1978-05-05', ' Australian ', 'Author 5'),  

('Lisa', 'F', '1990-06-06', 'Indian', 'Author 6'),  

('James', 'G', '1982-07-07', 'Australian', 'Author 7'),  

('Eric', 'H', '1988-08-08', 'American', 'Author 8');  

 

-- CATEGORIES  

INSERT INTO Category (name, description)  

VALUES  

('Fiction', 'Fiction books'),  

('Mystery', 'Mystery stories'),  

('Fantasy', 'Fantasy books'),  

('Biography', 'Life stories'),  

('Technology', 'Technical books');  

 

 -- BOOKS  

INSERT INTO Book  

(title, isbn, publication_date, total_copies, available_copies, library_id)  

VALUES  

('Harry Potter', 'ISBN001', '1997-06-26', 10, 7, 1),  

('The Da Vinci Code', 'ISBN002', '2003-04-01', 8, 5, 1),  

('The Alchemist', 'ISBN003', '1988-05-01', 7, 4, 1),  

('Wings of Fire', 'ISBN004', '1999-01-01', 9, 6, 1),  

('Clean Code', 'ISBN005', '2008-08-01', 6, 3, 1),  

('1984', 'ISBN006', '1949-06-08', 5, 2, 2),  

('Python Basics', 'ISBN007', '2019-01-10', 8, 5, 2),  

('Ikigai', 'ISBN008', '2016-01-01', 7, 4, 2),  

('Rich Dad Poor Dad', 'ISBN009', '1997-04-01', 10, 6, 2),  

('Atomic Habits', 'ISBN010', '2018-10-16', 9, 5, 2),  

('The Hobbit', 'ISBN011', '1937-09-21', 8, 4, 3),  

('Think and Grow Rich', 'ISBN012', '1937-01-01', 7, 3, 3),  

('Sapiens', 'ISBN013', '2011-01-01', 6, 2, 3),  

('Digital Fortress', 'ISBN014', '1998-02-01', 5, 2, 3),  

('The Silent Patient', 'ISBN015', '2019-02-05', 8, 5, 3);  

 

-- BOOKAUTHOR  

INSERT INTO BookAuthor (book_id, author_id)  

VALUES  

(1,1),  

(2,1),  

(3,2),  

(4,2),  

(5,3),  

(6,3),  

(7,4),  

(8,4),  

(9,5),  

(10,5),  

(11,6),  

(12,6),  

(13,7),  

(14,7),  

(15,8);  

 

 -- BOOKCATEGORY  

INSERT INTO BookCategory (book_id, category_id)  

VALUES 

(1,1),  

(2,1),  

(3,2),  

(4,2),  

(5,3),  

(6,3),  

(7,4),  

(8,4),  

(9,5),  

(10,5),  

(11,1),  

(12,2),  

(13,3),  

(14,4),  

(15,5);  

 

-- MEMBERS  

INSERT INTO Member  

(first_name, last_name, email, phone, member_type, registration_date)  

VALUES  

('Pavan', 'A', 'pavan@mail.com', '8000000001', 'student', '2025-01-01'),  

('Krishna', 'B', 'krishna@mail.com', '8000000002', 'student', '2025-01-02'),  

('Riya', 'C', 'riya@mail.com', '8000000003', 'faculty', '2025-01-03'),  

('Anu', 'D', 'anu@mail.com', '8000000004', 'student', '2025-01-04'),  

('Raj', 'E', 'raj@mail.com', '8000000005', 'faculty', '2025-01-05'),  

('Tina', 'F', 'tina@mail.com', '8000000006', 'student', '2025-01-06'),  

('Aman', 'G', 'aman@mail.com', '8000000007', 'student', '2025-01-07'),  

('Nina', 'H', 'nina@mail.com', '8000000008', 'faculty', '2025-01-08'),  

('Vijay', 'I', 'vijay@mail.com', '8000000009', 'student', '2025-01-09'),  

('Pooja', 'J', 'pooja@mail.com', '8000000010', 'student', '2025-01-10'),  

('Ravi', 'K', 'ravi@mail.com', '8000000011', 'faculty', '2025-01-11'),  

('Meena', 'L', 'meena@mail.com', '8000000012', 'student', '2025-01-12'),  

('Kiran', 'M', 'kiran@mail.com', '8000000013', 'student', '2025-01-13'),  

('Deepa', 'N', 'deepa@mail.com', '8000000014', 'faculty', '2025-01-14'),  

('Arun', 'O', 'arun@mail.com', '8000000015', 'student', '2025-01-15'),  

('Sita', 'P', 'sita@mail.com', '8000000016', 'student', '2025-01-16'),  

('Ajay', 'Q', 'ajay@mail.com', '8000000017', 'faculty', '2025-01-17'),  

('Neha', 'R', 'neha@mail.com', '8000000018', 'student', '2025-01-18'),  

('Manu', 'S', 'manu@mail.com', '8000000019', 'faculty', '2025-01-19'),  

('Lata', 'T', 'lata@mail.com', '8000000020', 'student', '2025-01-20');  

 

-- BORROWINGS  

INSERT INTO Borrowing  

(member_id, book_id, borrow_date, due_date, return_date, late_fee)  

VALUES  

(1,1,'2026-05-01','2026-05-10','2026-05-09',0),  

(2,2,'2026-05-02','2026-05-11','2026-05-12',10),  

(3,3,'2026-05-03','2026-05-12',NULL,20),  

(4,4,'2026-05-04','2026-05-13','2026-05-13',0),  

(5,5,'2026-05-05','2026-05-14',NULL,15),  

(6,6,'2026-05-06','2026-05-15',NULL,0),  

(7,7,'2026-05-07','2026-05-16','2026-05-18',5),  

(8,8,'2026-05-08','2026-05-17',NULL,25),  

(9,9,'2026-05-09','2026-05-18',NULL,0),  

(10,10,'2026-05-10','2026-05-19','2026-05-20',10),  

(11,11,'2026-05-11','2026-05-20',NULL,0),  

(12,12,'2026-05-12','2026-05-21',NULL,0),  

(13,13,'2026-05-13','2026-05-22','2026-05-22',0),  

(14,14,'2026-05-14','2026-05-23',NULL,30),  

(15,15,'2026-05-15','2026-05-24',NULL,20),  

(16,1,'2026-05-16','2026-05-25',NULL,0),  

(17,2,'2026-05-17','2026-05-26',NULL,0),  

(18,3,'2026-05-18','2026-05-27',NULL,5),  

(19,4,'2026-05-19','2026-05-28',NULL,0),  

(20,5,'2026-05-20','2026-05-29',NULL,10),  

(1,6,'2026-05-21','2026-05-30',NULL,0),  

(2,7,'2026-05-22','2026-05-31',NULL,0),  

(3,8,'2026-05-23','2026-06-01',NULL,0),  

(4,9,'2026-05-24','2026-06-02',NULL,0),  

(5,10,'2026-05-25','2026-06-03',NULL,0);  

 

 -- REVIEWS  

INSERT INTO Review  

(member_id, book_id, rating, comment, review_date)  

VALUES  

(1,1,5,'Good','2026-05-01'),  

(2,2,4,'Nice','2026-05-02'),  

(3,3,5,'Excellent','2026-05-03'),  

(4,4,4,'Helpful','2026-05-04'),  

(5,5,3,'Okay','2026-05-05'),  

(6,6,5,'Very good','2026-05-06'),  

(7,7,4,'Useful','2026-05-07'),  

(8,8,5,'Best','2026-05-08'),  

(9,9,4,'Simple','2026-05-09'),  

(10,10,3,'Average','2026-05-10'),  

(11,11,5,'Excellent','2026-05-11'),  

(12,12,4,'Good','2026-05-12');




-- VIEW ALL TABLES  

SELECT * FROM Library;  

SELECT * FROM Author;  

SELECT * FROM Category;  

SELECT * FROM Book;  

SELECT * FROM Member;  

SELECT * FROM Borrowing;  

SELECT * FROM Review;  

SELECT * FROM BookAuthor;  

SELECT * FROM BookCategory; 
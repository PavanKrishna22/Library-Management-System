-- 1. Books with Authors and Categories 

SELECT 

    b.book_id, 

    b.title, 

    CONCAT(a.first_name, ' ', a.last_name) AS author_name, 

    c.name AS category_name 

FROM Book b 

JOIN BookAuthor ba ON b.book_id = ba.book_id 

JOIN Author a ON ba.author_id = a.author_id 

JOIN BookCategory bc ON b.book_id = bc.book_id 

JOIN Category c ON bc.category_id = c.category_id 

ORDER BY b.book_id; 

 

-- 2. Most Borrowed Books 

SELECT 

    b.title, 

    COUNT(br.borrowing_id) AS total_borrows 

FROM Borrowing br 

JOIN Book b ON br.book_id = b.book_id 

GROUP BY b.book_id, b.title 

ORDER BY total_borrows DESC 

LIMIT 5; 

 

-- 3. Members with Overdue Books 

SELECT 

    m.member_id, 

    CONCAT(m.first_name, ' ', m.last_name) AS member_name, 

    b.title, 

    br.due_date, 

    DATEDIFF(CURDATE(), br.due_date) AS overdue_days, 

    DATEDIFF(CURDATE(), br.due_date) * 15 AS late_fee 

FROM Borrowing br 

JOIN Member m ON br.member_id = m.member_id 

JOIN Book b ON br.book_id = b.book_id 

WHERE br.return_date IS NULL 

AND br.due_date < CURDATE(); 

 

-- 4. Average Rating per Book 

SELECT 

    b.title, 

    CONCAT(a.first_name, ' ', a.last_name) AS author_name, 

    AVG(r.rating) AS avg_rating, 

    COUNT(r.review_id) AS total_reviews 

FROM Review r 

JOIN Book b ON r.book_id = b.book_id 

JOIN BookAuthor ba ON b.book_id = ba.book_id 

JOIN Author a ON ba.author_id = a.author_id 

GROUP BY  

    b.book_id,  

    b.title,  

    a.author_id,  

    a.first_name,  

    a.last_name 

ORDER BY avg_rating DESC; 

 

-- 5. Books Available in Each Library 

SELECT 

    l.name AS library_name, 

    b.title, 

    b.total_copies, 

    b.available_copies 

FROM Book b 

JOIN Library l ON b.library_id = l.library_id 

ORDER BY l.name; 

-- CTE  

-- Overdue Books List  

WITH OverdueBooks AS (  
   SELECT   
      m.member_id,  
       CONCAT(m.first_name, ' ', m.last_name) AS member_name,  
       b.title,  
       br.due_date  
   FROM Borrowing br  
   JOIN Member m ON br.member_id = m.member_id  
   JOIN Book b ON br.book_id = b.book_id  
   WHERE br.return_date IS NULL  
     AND br.due_date < CURDATE()  
)  
SELECT * FROM OverdueBooks; 

 

-- Transaction 

-- When a user borrows a book, update stock and create borrowing record 

START TRANSACTION; 

UPDATE Book 

SET available_copies = available_copies - 1 

WHERE book_id = 1; 

INSERT INTO Borrowing (member_id, book_id, borrow_date, due_date, late_fee) 

VALUES (1, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY), 0); 

 

-- ROLLBACK; 

COMMIT; 

 

 

 

-- Window Function 

-- Track borrowing growth over time 

SELECT 

borrow_date, 

COUNT(*) AS daily_borrows, 

SUM(COUNT(*)) OVER ( 

ORDER BY borrow_date 

) AS running_total 

FROM Borrowing 

GROUP BY borrow_date;




-- ========================================

SELECT
    b.title,
    r.rating,

    AVG(r.rating) OVER (
        PARTITION BY b.book_id
    ) AS avg_book_rating
FROM Review r
JOIN Book b
    ON r.book_id = b.book_id;
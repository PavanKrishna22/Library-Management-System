-- LIBRARY MANAGEMENT SYSTEM (LMS) Assessment-1, Phase-1 

 

CREATE DATABASE IF NOT EXISTS LMS_DB; 

-- DROP DATABASE LMS_DB; 

USE LMS_DB; 

 

-- LIBRARY TABLE 

CREATE TABLE Library ( 

    library_id INT AUTO_INCREMENT PRIMARY KEY, 

    name VARCHAR(150) NOT NULL, 

    campus_location VARCHAR(200) NOT NULL, 

    contact_email VARCHAR(150) NOT NULL UNIQUE, 

    phone_number VARCHAR(20) UNIQUE, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 

); 

 

-- AUTHOR TABLE 

CREATE TABLE Author ( 

    author_id INT AUTO_INCREMENT PRIMARY KEY, 

    first_name VARCHAR(100) NOT NULL, 

    last_name VARCHAR(100) NOT NULL, 

    birth_date DATE, 

    nationality VARCHAR(100), 

    biography TEXT, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 

); 

 

-- CATEGORY TABLE 

CREATE TABLE Category ( 

    category_id INT AUTO_INCREMENT PRIMARY KEY, 

    name VARCHAR(100) NOT NULL UNIQUE, 

    description TEXT, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 

); 

 

-- MEMBER TABLE 

CREATE TABLE Member ( 

    member_id INT AUTO_INCREMENT PRIMARY KEY, 

    first_name VARCHAR(100) NOT NULL, 

    last_name VARCHAR(100) NOT NULL, 

    email VARCHAR(150) NOT NULL UNIQUE, 

    phone VARCHAR(20) UNIQUE, 

    member_type VARCHAR(20) NOT NULL, 

    registration_date DATE NOT NULL, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 

 

    CHECK (member_type IN ('student', 'faculty')) 

); 

 

-- BOOK TABLE 

CREATE TABLE Book ( 

    book_id INT AUTO_INCREMENT PRIMARY KEY, 

    title VARCHAR(255) NOT NULL, 

    isbn VARCHAR(20) NOT NULL UNIQUE, 

    publication_date DATE, 

    total_copies INT NOT NULL DEFAULT 1, 

    available_copies INT NOT NULL DEFAULT 1, 

    library_id INT NOT NULL, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 

 

    FOREIGN KEY (library_id) REFERENCES Library(library_id) ON DELETE CASCADE, 

 

    CHECK (total_copies >= 0), 

    CHECK (available_copies >= 0 AND available_copies <= total_copies) 

); 

 

-- BORROWING TABLE 

CREATE TABLE Borrowing ( 

    borrowing_id INT AUTO_INCREMENT PRIMARY KEY, 

    member_id INT NOT NULL, 

    book_id INT NOT NULL, 

    borrow_date DATE NOT NULL, 

    due_date DATE NOT NULL, 

    return_date DATE, 

    late_fee DECIMAL(8,2) DEFAULT 0.00, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 

 

    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE, 

    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE, 

 

    CHECK (due_date >= borrow_date), 

    CHECK (late_fee >= 0) 

); 

 

-- REVIEW TABLE 

CREATE TABLE Review ( 

    review_id INT AUTO_INCREMENT PRIMARY KEY, 

    member_id INT NOT NULL, 

    book_id INT NOT NULL, 

    rating INT NOT NULL, 

    comment TEXT, 

    review_date DATE NOT NULL, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 

 

    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE, 

 

    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE, 

 

    CHECK (rating BETWEEN 1 AND 5), 

    UNIQUE (member_id, book_id) 

); 

 

-- BOOKAUTHOR TABLE 

CREATE TABLE BookAuthor ( 

    book_id INT NOT NULL, 

    author_id INT NOT NULL, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 

 

    PRIMARY KEY (book_id, author_id), 

 

    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE, 

    FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE 

); 

 

-- BOOKCATEGORY TABLE 

CREATE TABLE BookCategory ( 

    book_id INT NOT NULL, 

    category_id INT NOT NULL, 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 

 

    PRIMARY KEY (book_id, category_id), 

 

    FOREIGN KEY (book_id) REFERENCES Book(book_id)ON DELETE CASCADE, 

    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE 

);
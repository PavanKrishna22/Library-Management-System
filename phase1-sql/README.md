# Phase 1: Database Design & SQL Implementation

## Overview

This phase implements the database layer for the Library Management System (LMS). The objective is to design a normalized relational database capable of managing libraries, books, authors, members, borrowing activities, and reviews.

The implementation demonstrates SQL database design principles, relational modeling, and advanced SQL querying.

---

## Features

* Normalized relational database design
* Primary and foreign key relationships
* Many-to-many relationships using junction tables
* Data integrity through constraints
* Sample data for testing
* Analytical SQL queries
* Common Table Expressions (CTEs)
* Window functions
* Transaction management

---

## Database Schema

The database consists of the following tables:

* Library
* Author
* Category
* Book
* BookAuthor
* BookCategory
* Member
* Borrowing
* Review

### Relationships

* A library contains many books.
* A book can have multiple authors.
* A book can belong to multiple categories.
* Members can borrow multiple books.
* Members can review books.
* Borrowing records track issued and returned books.

---

## Files

| File        | Description                            |
| ----------- | -------------------------------------- |
| schema.sql  | Creates the database schema and tables |
| data.sql    | Inserts sample data                    |
| queries.sql | Analytical and reporting SQL queries   |

---

## SQL Concepts Demonstrated

### Database Design

* Primary Keys
* Foreign Keys
* Composite Keys
* Unique Constraints
* Check Constraints
* Cascading Deletes

### Advanced SQL

* JOIN operations
* Aggregate functions
* GROUP BY
* ORDER BY
* Common Table Expressions (CTEs)
* Window Functions
* Transactions

---

## Sample Queries

The project includes queries for:

* Books with authors and categories
* Most borrowed books
* Overdue members
* Average book ratings
* Books available in each library
* Running borrowing totals
* Overdue book reports

---

## How to Run

### 1. Create the database

Run:

```
schema.sql
```

### 2. Insert sample data

Run:

```
data.sql
```

### 3. Execute analytical queries

Run:

```
queries.sql
```

---

## Technologies

* MySQL
* SQL

---

## Learning Outcomes

This phase demonstrates:

* Relational database design
* Database normalization
* SQL data manipulation
* Complex query writing
* Transaction handling
* Analytical SQL techniques

---

# Author

**Pavan Krishna O**

This repository documents my learning journey and practical implementation of modern backend development concepts through the development of a complete Library Management System.

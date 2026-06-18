# Library Management System

A multi-phase **Library Management System** developed during my internship to gain practical experience in backend development, database design, ETL workflows, ORM frameworks, and REST API development using modern Python technologies.

---

## Project Overview

This project was developed as a structured backend engineering exercise and is divided into three progressive phases. Each phase builds upon the previous one, gradually evolving from database design to data ingestion and finally to a fully functional REST API.

The project demonstrates practical implementation of:

* Relational database design
* SQL schema development
* Data manipulation and querying
* ETL (Extract, Transform, Load) pipelines
* Data validation and normalization
* SQLAlchemy ORM
* External API integration
* Django REST Framework
* RESTful API development
* Testing and software engineering best practices

---

## Objectives

The primary goals of this project were to:

* Design a normalized relational database.
* Build reliable data ingestion pipelines.
* Validate and clean noisy datasets.
* Integrate external data sources.
* Develop RESTful APIs.
* Implement backend business logic.
* Practice software testing and project organization.

---

# System Architecture

The project follows a layered backend architecture.

```
                    External Data Sources
                    ┌───────────────┐
                    │ CSV Files     │
                    │ Open Library  │
                    └───────┬───────┘
                            │
                            ▼
                  Data Validation Layer
                            │
                            ▼
                    ETL Processing
                            │
                            ▼
                    SQLAlchemy ORM
                            │
                            ▼
                    Relational Database
                            │
                            ▼
                    Django Models
                            │
                            ▼
                  Django REST Framework
                            │
                            ▼
                     REST API Endpoints
                            │
                            ▼
                      API Consumers
```

---

# Repository Structure

```
Library-Management-System/

├── TASK_1/
│   ├── schema.sql
│   ├── data.sql
│   └── queries.sql
│
├── TASK_2/
│   └── library-etl/
│
└── TASK_3/
    └── LibraryManagementSystem/
```

---

# Phase 1: Database Design and SQL

## Overview

The first phase focuses on designing and implementing a relational database for the Library Management System.

The database models the core entities involved in a library ecosystem and establishes relationships between them.

## Entities

* Library
* Book
* Author
* Category
* Member
* Borrowing
* Review
* BookAuthor
* BookCategory

## Relationships

### One-to-Many

* Library → Books
* Member → Borrowings
* Member → Reviews

### Many-to-Many

* Books ↔ Authors
* Books ↔ Categories

### One-to-One Constraint

* One member can review a particular book only once.

---

## Database Features

The schema implementation includes:

* Primary keys
* Foreign keys
* Unique constraints
* CHECK constraints
* Timestamp tracking
* Referential integrity

---

## Data Population

Sample data was created for:

* Libraries
* Books
* Authors
* Categories
* Members
* Borrowings
* Reviews

---

## SQL Operations

Complex SQL queries demonstrate:

* Multi-table JOINs
* Aggregation functions
* Common Table Expressions
* Subqueries
* Window functions
* Transaction management

---

# Phase 2: Data Ingestion Pipeline

## Overview

The second phase implements a Python ETL pipeline for importing and processing library data.

The ETL system extracts data from CSV files and external APIs, validates and transforms the information, and loads it into the database.

---

## CSV Processing

The pipeline processes noisy CSV datasets containing:

* Libraries
* Books
* Authors
* Members

---

## Data Validation

Pydantic schemas are used for:

### ISBN Validation

* ISBN-10
* ISBN-13
* Check digit verification

### Email Validation

* Invalid email detection
* Standardized formatting

### Name Normalization

* Title casing
* Duplicate handling
* Whitespace cleanup

### Phone Validation

* Digit extraction
* Standard formatting

---

## SQLAlchemy ORM

Database operations include:

* ORM models
* Transactions
* Duplicate prevention
* Indexing
* Safe inserts

---

## External API Integration

The Open Library API integration performs:

### Author Search

Search for authors.

### Work Retrieval

Fetch books.

### Book Details

Retrieve detailed metadata.

### Data Validation

Normalize and validate responses.

### Database Storage

Store processed information.

---

## Error Handling

The ETL pipeline includes:

* Logging
* Exception handling
* Processing summaries
* Invalid record tracking

---

# Phase 3: Django REST API

## Overview

The final phase transforms the backend into a RESTful API using Django and Django REST Framework.

---

## Django Models

Models represent:

* Libraries
* Books
* Authors
* Categories
* Members
* Borrowings
* Reviews

---

## Serializers

Serializers provide:

* Validation
* Data conversion
* Nested representations

---

## REST API Endpoints

CRUD operations are implemented for:

```
/api/libraries/
/api/books/
/api/authors/
/api/categories/
/api/members/
/api/borrowings/
/api/reviews/
```

---

## Advanced Features

The API supports:

### Book Search

Search by:

* Title
* Author
* Category

### Availability Checking

Determine current stock.

### Borrowing

Issue books.

### Returning

Return borrowed books.

### Member History

Retrieve borrowing history.

### Statistics

Generate library analytics.

---

## Testing

The project includes:

* Model tests
* Serializer tests
* API tests

Testing focuses on:

* Validation
* Business logic
* Endpoint behavior
* Data integrity

---

# Technology Stack

| Category           | Technology            |
| ------------------ | --------------------- |
| Language           | Python                |
| Database           | SQL                   |
| ORM                | SQLAlchemy            |
| Framework          | Django                |
| API                | Django REST Framework |
| Validation         | Pydantic              |
| HTTP Client        | Requests              |
| Data Format        | JSON                  |
| Version Control    | Git                   |
| Repository Hosting | GitHub                |

---

# Key Features

* Relational database design
* SQL schema implementation
* Complex SQL queries
* ETL workflows
* CSV data processing
* Data validation
* External API integration
* SQLAlchemy ORM
* REST API development
* CRUD operations
* Automated testing
* Modular project structure

---

# Skills Demonstrated

This project provided practical experience with:

## Database Engineering

* Schema design
* Relationships
* Constraints
* SQL optimization

## Backend Development

* Python
* Django
* REST APIs

## ORM Development

* SQLAlchemy
* Model relationships
* Transaction management

## ETL Processes

* Data extraction
* Transformation
* Validation
* Loading

## API Integration

* HTTP requests
* JSON processing
* External services

## Software Engineering

* Testing
* Error handling
* Logging
* Project organization
* Version control

---

# Project Workflow

The development process follows three progressive stages:

```
Phase 1
Database Design
        │
        ▼
Phase 2
Data Ingestion
        │
        ▼
Phase 3
REST API Development
        │
        ▼
Complete Backend System
```

Each phase builds upon the previous one, resulting in an integrated backend solution for managing library operations.

---

# Future Enhancements

Potential improvements include:

* JWT authentication
* Role-based access control
* Recommendation engine
* Advanced analytics
* Docker containerization
* CI/CD pipelines
* API rate limiting
* Background task processing
* Deployment to cloud platforms

---

# Internship Project

This project was developed during my internship as part of a structured backend development program. The objective was to gain practical experience in designing relational databases, building ETL pipelines, integrating external APIs, implementing ORM-based data management, and developing RESTful services using Django REST Framework.

---

# Author

**Pavan Krishna O**

This repository documents my learning journey and practical implementation of modern backend development concepts through the development of a complete Library Management System.
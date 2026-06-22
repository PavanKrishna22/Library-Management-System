# 📚 Library Management System – Phase 3

A production-style **Django REST Framework API** for managing libraries, books, authors, members, borrowings, and reviews.

This project extends the previous ETL pipeline by providing a fully functional REST API with authentication, filtering, searching, borrowing workflows, recommendations, statistics, and interactive API documentation.

---

# Features

## Core Management

* Library management
* Author management
* Category management
* Book management
* Member management
* Borrowing management
* Review management

---

## Book Operations

* Check book availability
* Borrow books
* Return books
* Search books
* Book recommendations

---

## API Features

* RESTful CRUD APIs
* Pagination
* Filtering
* Searching
* Ordering
* Nested serializers
* Custom API endpoints
* Authentication
* OpenAPI documentation

---

## Documentation

* Swagger UI
* ReDoc UI
* OpenAPI schema generation

---

## Testing

* Model tests
* Serializer tests
* API tests

---

# Project Structure

```
phase3-django-api/

│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── library/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── ...
│
├── manage.py
├── .env
└── README.md
```

---

# Technology Stack

## Backend

* Python
* Django
* Django REST Framework

## Database

* PostgreSQL

## API Documentation

* drf-spectacular
* Swagger UI
* ReDoc

## Authentication

* Session Authentication
* Basic Authentication

## Filtering

* django-filter

## Testing

* Django Test Framework
* DRF APITestCase

---

# Database Models

## Library

Stores:

* Name
* Campus location
* Contact email
* Phone number

---

## Author

Stores:

* First name
* Last name
* Birth date
* Nationality
* Biography

---

## Category

Stores book categories such as:

* Fiction
* Mystery
* Fantasy
* Science

---

## Book

Stores:

* Title
* ISBN
* Publication date
* Total copies
* Available copies
* Library

Supports availability checking.

---

## Member

Supports:

* Student members
* Faculty members

---

## Borrowing

Tracks:

* Borrow date
* Due date
* Return date
* Late fee

---

## Review

Stores:

* Rating
* Comment
* Review date

One review per member per book.

---

# API Endpoints

## System

| Method | Endpoint         |
| ------ | ---------------- |
| GET    | /api/            |
| GET    | /api/statistics/ |

---

## Libraries

```
GET     /api/libraries/
POST    /api/libraries/

GET     /api/libraries/{id}/
PUT     /api/libraries/{id}/
PATCH   /api/libraries/{id}/
DELETE  /api/libraries/{id}/
```

---

## Authors

```
GET
POST
PUT
PATCH
DELETE
```

```
/api/authors/
```

---

## Categories

```
/api/categories/
```

Full CRUD supported.

---

## Members

```
/api/members/
```

Supports:

* filtering
* searching
* ordering

Extra endpoint:

```
GET /api/members/{id}/borrowings/
```

Returns member borrowing history.

---

## Books

```
/api/books/
```

Supports:

* CRUD
* filtering
* searching
* ordering

### Availability

```
GET /api/books/{id}/availability/
```

Returns:

```
{
    total_copies,
    available_copies,
    available
}
```

---

### Borrow Book

```
POST /api/books/borrow/
```

Request:

```
{
    "member_id":1,
    "book_id":5
}
```

Automatically:

* creates borrowing
* decreases available copies

---

### Return Book

```
POST /api/books/return/
```

Request:

```
{
    "borrowing_id":10
}
```

Automatically:

* sets return date
* increases available copies

---

### Search Books

```
GET /api/books/search/?search=python
```

Searches:

* title
* author
* category

---

### Book Recommendations

```
GET /api/books/recommendations/?member_id=1
```

Recommendations are based on:

* borrowing history
* categories
* ratings
* popularity
* availability

---

## Borrowings

```
/api/borrowings/
```

Supports:

* CRUD
* filtering
* searching
* ordering

---

## Reviews

```
/api/reviews/
```

Supports:

* CRUD
* filtering
* searching
* ordering

---

# Statistics Endpoint

```
GET /api/statistics/
```

Returns:

```
{
    total_libraries,
    total_books,
    total_authors,
    total_categories,
    total_members,
    total_borrowings,
    total_reviews,
    books_available,
    books_borrowed
}
```

---

# Authentication

The API supports:

## Session Authentication

Useful for:

* Admin panel
* Swagger UI

---

## Basic Authentication

Useful for:

* API clients
* Testing

Permissions:

```
IsAuthenticatedOrReadOnly
```

Authenticated users:

* Create
* Update
* Delete

Anonymous users:

* Read-only access

---

# Filtering, Searching and Ordering

## Books

Filter:

```
library
```

Search:

```
title
isbn
```

Order:

```
title
publication_date
available_copies
```

---

## Members

Filter:

```
member_type
```

Search:

```
first_name
last_name
email
```

---

## Borrowings

Filter:

```
member
book
```

---

## Reviews

Filter:

```
member
book
rating
```

---

# Swagger Documentation

Generate schema:

```
/api/schema/
```

Swagger UI:

```
/api/docs/swagger/
```

ReDoc:

```
/api/docs/redoc/
```

Interactive documentation includes:

* Request bodies
* Response schemas
* Parameters
* Examples
* Authentication

---

# Running the Project

## Clone

```
git clone <repository-url>

cd phase3-django-api
```

---

## Create Virtual Environment

```
python -m venv .venv
```

Activate:

Windows:

```
.venv\Scripts\activate
```

Linux/Mac:

```
source .venv/bin/activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

## Configure Environment

Create:

```
.env
```

Example:

```
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

## Apply Migrations

```
python manage.py makemigrations

python manage.py migrate
```

---

## Create Superuser

```
python manage.py createsuperuser
```

---

## Run Server

```
python manage.py runserver
```

API:

```
http://127.0.0.1:8000/api/
```

Swagger:

```
http://127.0.0.1:8000/api/docs/swagger/
```

ReDoc:

```
http://127.0.0.1:8000/api/docs/redoc/
```

---

# Running Tests

Run all tests:

```
python manage.py test
```

Includes:

* Model tests
* Serializer tests
* API tests

---

# Highlights

## Custom Endpoints

* Health check
* Statistics
* Book availability
* Borrow book
* Return book
* Search books
* Book recommendations
* Member borrowing history

---

## Advanced Features

* Nested serializers
* ORM queries
* Raw SQL joins
* Pagination
* Authentication
* Filtering
* Ordering
* Swagger documentation
* Recommendation engine

---

# Future Improvements

Potential enhancements:

* JWT Authentication
* Automatic late fee calculation
* Fine payment gateway
* Reservation system
* Email notifications
* Inventory analytics
* Docker deployment
* CI/CD pipeline
* Redis caching

---

# Learning Outcomes

This project demonstrates practical experience with:

* Django
* Django REST Framework
* PostgreSQL
* REST API design
* Authentication
* API documentation
* Database modeling
* ORM
* Raw SQL
* Testing
* Filtering and pagination
* Nested serialization
* Custom DRF actions
* Production-style backend architecture

---

# Author

**Pavan Krishna O**

This repository documents my learning journey and practical implementation of modern backend development concepts through the development of a complete Library Management System.

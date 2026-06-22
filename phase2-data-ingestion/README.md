# Phase 2 – Data Ingestion (Python ETL)

## Overview

This phase implements a Python-based ETL (Extract, Transform, Load) pipeline for the Library Management System.

The project performs the following tasks:

- Reads library data from CSV files.
- Validates records using Pydantic.
- Cleans and normalizes input data.
- Loads validated records into a relational database using SQLAlchemy.
- Integrates with the Open Library API to fetch author and book information.
- Prevents duplicate records from being inserted.
- Logs processing details and validation errors.

---

## Features

### CSV ETL Pipeline

- Reads multiple CSV files.
- Data validation using Pydantic.
- Invalid records are skipped.
- Duplicate detection.
- Inserts valid data into the database.

Supported datasets:

- Libraries
- Authors
- Books
- Members

---

## Open Library API Integration

The project can:

- Search authors.
- Fetch author works.
- Retrieve work details.
- Save raw API responses as JSON.
- Validate fetched book data.
- Store validated records in the database.

---

## Technologies Used

- Python
- SQLAlchemy
- Pydantic
- Requests
- PostgreSQL
- Logging
- argparse

---

## Project Structure

```

phase2-data-ingestion/
│
├── CSV_DATA/
├── api_client.py
├── api_fetcher.py
├── database.py
├── models.py
├── schemas.py
├── main.py
├── books.json
└── README.md

```

---

## Running the CSV ETL

```
python main.py \
--directory CSV_DATA \
--database-url DATABASE_URL
```

Example:

```
python main.py --directory CSV_DATA --database-url postgresql://user:password@localhost/library_db
```

---

## Running the Open Library API Fetcher

```
python api_fetcher.py \
--author "J.K. Rowling" \
--limit 10 \
--database-url DATABASE_URL \
--output books.json
```

Example:

```
python api_fetcher.py --author "George Orwell" --limit 5 --database-url postgresql://user:password@localhost/library_db --output books.json
```

---

## Data Validation

Pydantic is used to validate:

- Names
- Emails
- Phone numbers
- ISBN values
- Dates

Invalid records are logged and skipped.

---

## Database Operations

SQLAlchemy ORM is used to:

- Create tables
- Manage sessions
- Insert records
- Detect duplicates

---

## Logging

The ETL pipeline logs:

- File processing
- Validation failures
- Duplicate records
- Database insertions
- API requests
- Processing summaries

---

## Outcome

This phase demonstrates a complete ETL workflow by combining:

- CSV ingestion
- Data validation
- Data normalization
- Database persistence
- External API integration
- Error handling
- Logging

---

# Author

**Pavan Krishna O**

This repository documents my learning journey and practical implementation of modern backend development concepts through the development of a complete Library Management System.

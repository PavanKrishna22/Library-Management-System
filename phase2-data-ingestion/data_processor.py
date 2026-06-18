import argparse
import csv
import os
import logging
from datetime import datetime

from pydantic import ValidationError

from schemas import Member as MemberSchema, Book as BookSchema, Author as AuthorSchema, Library as LibrarySchema
from models import Member as MemberModel, Book as BookModel, Author as AuthorModel, Library as LibraryModel

from database import get_engine, get_session, create_tables

# -------------------------
# CLI PARSER
# -------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ETL pipeline: CSV → Pydantic validation → Database"
    )
    parser.add_argument("--directory", "-d", required=True)
    parser.add_argument("--database-url", "--db", required=True)
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO"
    )
    return parser.parse_args()

# -------------------------
# SCHEMA ROUTER
# -------------------------
def get_schema(file_name):
    if file_name == "members.csv":
        return MemberSchema
    elif file_name == "books.csv":
        return BookSchema
    elif file_name == "authors.csv":
        return AuthorSchema
    elif file_name == "libraries.csv":
        return LibrarySchema
    else:
        return None

# -------------------------
# DATABASE INSERTION
# -------------------------
def insert_records(session, records):
    inserted = 0
    skipped = 0

    for record in records:
        try:
            if isinstance(record, LibrarySchema):

                existing = session.query(
                    LibraryModel
                ).filter_by(
                    library_id=record.library_id
                ).first()

                if existing:
                    logging.info(
                        "Duplicate library skipped."
                    )
                    skipped += 1
                    continue

            db_obj = None
            if isinstance(record, LibrarySchema):
                db_obj = LibraryModel(
                    library_id=record.library_id,
                    name=record.name,
                    campus_location=record.campus_location,
                    contact_email=record.contact_email,
                    phone_number=record.phone_number
                )
            elif isinstance(record, BookSchema):
                if record.isbn:

                    existing = session.query(
                        BookModel
                    ).filter_by(
                        isbn=record.isbn
                    ).first()

                else:

                    existing = session.query(
                        BookModel
                    ).filter_by(
                        title=record.title
                    ).first()

                if existing:
                    logging.info(
                        "Duplicate book skipped."
                    )
                    skipped += 1
                    continue

                pub_date = None
                if record.publication_date:
                    try:
                        pub_date = datetime.strptime(record.publication_date, "%Y-%m-%d").date()
                    except Exception:
                        pass
                db_obj = BookModel(
                    book_id=record.book_id,
                    title=record.title,
                    isbn=record.isbn,
                    publication_date=pub_date,
                    total_copies=(
                        int(record.total_copies)
                        if record.total_copies
                        else None
                    ),
                    available_copies=(
                        int(record.available_copies)
                        if record.available_copies
                        else None
                    ),
                    library_id=(
                        int(record.library_id)
                        if record.library_id
                        else None
                    )
                )
            elif isinstance(record, AuthorSchema):
                existing = session.query(
                    AuthorModel
                ).filter_by(
                    author_id=record.author_id
                ).first()

                if existing:
                    logging.info(
                        "Duplicate author skipped."
                    )
                    skipped += 1
                    continue

                db_obj = AuthorModel(
                    author_id=record.author_id,
                    first_name=record.first_name,
                    last_name=record.last_name,
                    birth_date=record.birth_date,
                    nationality=record.nationality,
                    biography=record.biography
                )
            elif isinstance(record, MemberSchema):
                existing = session.query(
                    MemberModel
                ).filter_by(
                    email=record.email
                ).first()

                if existing:
                    logging.info(
                        "Duplicate member skipped."
                    )
                    skipped += 1
                    continue

                db_obj = MemberModel(
                    member_id=record.member_id,
                    first_name=record.first_name,
                    last_name=record.last_name,
                    email=record.email,
                    phone=record.phone,
                    member_type=record.member_type,
                    registration_date=record.registration_date,
                    library_id=None
                )
            else:
                skipped += 1
                continue

            session.add(db_obj)
            session.commit()
            inserted += 1

        except Exception as e:
            session.rollback()
            skipped += 1
            logging.warning("Skipping record due to insert error: %s", e)

    return inserted, skipped

# -------------------------
# MAIN ETL PROCESS
# -------------------------
def main():
    args = parse_arguments()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    db_url = args.database_url
    engine = get_engine(db_url)
    create_tables(engine)
    session = get_session(engine)

    directory = args.directory
    csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    logger.info("CSV files found: %s", csv_files)

    # Ensure correct FK order: libraries → authors → books → members
    csv_files.sort(key=lambda x: ["libraries.csv", "authors.csv", "books.csv", "members.csv"].index(x))

    for file in csv_files:
        file_path = os.path.join(directory, file)
        schema = get_schema(file)

        if schema is None:
            logger.warning("Skipping unknown file: %s", file)
            continue

        valid_records = []
        invalid_records = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    obj = schema(**row)
                    valid_records.append(obj)
                except ValidationError as e:
                    invalid_records.append({"row": row, "error": str(e)})
                    logger.warning("Validation failed: %s | Error: %s", row, e)

        inserted, skipped = insert_records(session, valid_records)
        logger.info("%s: Inserted=%d, Skipped=%d", file, inserted, skipped)

        logger.info("===================================")
        logger.info("FILE: %s", file)
        logger.info("Total Valid: %d", len(valid_records))
        logger.info("Total Invalid: %d", len(invalid_records))
        logger.info("===================================")

if __name__ == "__main__":
    main()
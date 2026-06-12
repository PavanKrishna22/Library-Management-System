import argparse
import logging
import json

from pydantic import ValidationError

from api_client import OpenLibraryClient
from schemas import Book as BookSchema

from database import (
    get_engine,
    get_session,
    create_tables
)

from models import Book as BookModel

# -------------------------------------------------
# CLI
# -------------------------------------------------

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Fetch book data from Open Library API"
    )

    parser.add_argument(
        "--author",
        required=True,
        help="Author name"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum books to fetch"
    )

    parser.add_argument(
        "--database-url",
        "--db",
        required=True,
        help="Database URL"
    )

    parser.add_argument(
        "--output",
        help="Optional JSON output file"
    )

    return parser.parse_args()


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():

    args = parse_arguments()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    client = OpenLibraryClient()

    engine = get_engine(args.database_url)

    create_tables(engine)

    session = get_session(engine)

    validated_books = []
    invalid_books = []

    raw_data = {
        "author_search_response": None,
        "author_works_response": None,
        "work_details": []
    }

    # -------------------------------------------------
    # SEARCH AUTHOR
    # -------------------------------------------------

    logging.info(
        "Searching author: %s",
        args.author
    )

    author_response = client.search_author(
        args.author
    )

    raw_data["author_search_response"] = author_response

    if author_response is None:
        logging.error(
            "Author search failed."
        )
        return

    authors = author_response.get(
        "docs",
        []
    )

    if not authors:
        logging.warning(
            "No author found."
        )
        return

    author = authors[0]

    author_key = author.get(
        "key"
    )

    logging.info(
        "Author found."
    )

    logging.info(
        "Name: %s",
        author.get("name")
    )

    logging.info(
        "Author Key: %s",
        author_key
    )

    logging.info(
        "Birth Date: %s",
        author.get("birth_date")
    )

    logging.info(
        "Work Count: %s",
        author.get("work_count")
    )

    # -------------------------------------------------
    # FETCH WORKS
    # -------------------------------------------------

    logging.info(
        "Fetching author works..."
    )

    works_response = client.get_author_works(
        author_key
    )

    raw_data["author_works_response"] = works_response

    if works_response is None:
        logging.error(
            "Failed to fetch works."
        )
        return

    works = works_response.get(
        "entries",
        []
    )

    works = works[:args.limit]

    logging.info(
        "Works fetched: %d",
        len(works)
    )

    # -------------------------------------------------
    # FETCH WORK DETAILS
    # -------------------------------------------------

    for index, work in enumerate(
        works,
        start=1
    ):

        title = work.get(
            "title"
        )

        work_key = work.get(
            "key",
            ""
        )

        work_key = work_key.replace(
            "/works/",
            ""
        )

        logging.info(
            "================================="
        )

        logging.info(
            "Book %d",
            index
        )

        logging.info(
            "Title: %s",
            title
        )

        logging.info(
            "Work Key: %s",
            work_key
        )

        details = client.get_work_details(
            work_key
        )

        if details is None:
            logging.warning(
                "Could not fetch work details."
            )
            continue

        raw_data["work_details"].append(
            details
        )

                # -----------------------------
        # Validate using existing schema
        # -----------------------------

        try:

            book = BookSchema(
                book_id=index,
                title=title,
                isbn=None,
                publication_date=None,
                total_copies=None,
                available_copies=None,
                library_id=None
            )

            validated_books.append(book)

            logging.info(
                "Book validated successfully."
            )

            existing = session.query(
                BookModel
            ).filter_by(
                title=book.title
            ).first()

            if existing:

                logging.info(
                    "Duplicate book skipped."
                )

            else:

                db_book = BookModel(
                    title=book.title,
                    isbn=book.isbn,
                    publication_date=book.publication_date,
                    total_copies=book.total_copies,
                    available_copies=book.available_copies,
                    library_id=book.library_id
                )

                try:
                    session.add(db_book)
                    session.commit()

                    logging.info(
                        "Book inserted into database."
                    )

                except Exception as e:

                    session.rollback()

                    logging.warning(
                        "Database insert failed: %s",
                        e
                    )

        except ValidationError as e:

            invalid_books.append(
                {
                    "title": title,
                    "error": str(e)
                }
            )

            logging.warning(
                "Validation failed: %s",
                title
            )

        description = details.get(
            "description"
        )

        if isinstance(
            description,
            dict
        ):
            description = description.get(
                "value"
            )

        created = details.get(
            "created",
            {}
        )

        created_date = created.get(
            "value"
        )

        subjects = details.get(
            "subjects",
            []
        )

        logging.info(
            "Created: %s",
            created_date
        )

        logging.info(
            "Subjects: %s",
            ", ".join(subjects[:5])
            if subjects
            else "None"
        )

        logging.info(
            "Description: %s",
            description
            if description
            else "None"
        )

    logging.info(
            "================================="
        )

    logging.info(
        "Validation Summary"
    )

    logging.info(
        "Valid Books: %d",
        len(validated_books)
    )

    logging.info(
        "Invalid Books: %d",
        len(invalid_books)
    )

    logging.info(
        "================================="
    )        

    # -------------------------------------------------
    # SAVE RAW JSON
    # -------------------------------------------------

    if args.output:

        with open(
            args.output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                raw_data,
                f,
                indent=4,
                ensure_ascii=False
            )

        logging.info(
            "Raw API responses saved to %s",
            args.output
        )

    session.close()


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    main()
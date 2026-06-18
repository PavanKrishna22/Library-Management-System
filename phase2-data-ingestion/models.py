from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Index

# engine (db connection layer)
# base (orm foundation)
# models (tables definition)
# session (manages the transactions)


class Base(DeclarativeBase):
    pass


book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.book_id"), primary_key=True),
    Column("author_id", ForeignKey("authors.author_id"), primary_key=True)
)


# =====================================================
# LIBRARY
# =====================================================

class Library(Base):
    __tablename__ = "libraries"

    library_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)
    campus_location = Column(String(255))

    contact_email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)

    # relationships
    books = relationship(
        "Book",
        back_populates="library"
    )

    members = relationship(
        "Member",
        back_populates="library"
    )


# =====================================================
# BOOK
# =====================================================

class Book(Base):
    __tablename__ = "books"

    book_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    # OpenLibrary may not always provide ISBN
    isbn = Column(
        String(20),
        unique=True,
        nullable=True
    )

    publication_date = Column(Date)

    total_copies = Column(Integer)
    available_copies = Column(Integer)

    # API books may not belong to a local library
    library_id = Column(
        Integer,
        ForeignKey("libraries.library_id"),
        nullable=True
    )

    # relationships
    library = relationship(
        "Library",
        back_populates="books"
    )

    authors = relationship(
        "Author",
        secondary=book_author,
        back_populates="books"
    )

    # index for fast lookup
    __table_args__ = (
        Index(
            "idx_books_isbn",
            "isbn"
        ),
    )


# =====================================================
# AUTHOR
# =====================================================

class Author(Base):
    __tablename__ = "authors"

    author_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    birth_date = Column(Date)

    nationality = Column(String(100))

    biography = Column(String)

    books = relationship(
        "Book",
        secondary=book_author,
        back_populates="authors"
    )

    # index for searching authors
    __table_args__ = (
        Index(
            "idx_author_name",
            "last_name",
            "first_name"
        ),
    )


# =====================================================
# MEMBER
# =====================================================

class Member(Base):
    __tablename__ = "members"

    member_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True
    )

    phone = Column(
        String(20),
        nullable=False
    )

    member_type = Column(String(50))

    registration_date = Column(Date)

    library_id = Column(
        Integer,
        ForeignKey("libraries.library_id")
    )

    library = relationship(
        "Library",
        back_populates="members"
    )

    # index for fast email lookup
    __table_args__ = (
        Index(
            "idx_member_email",
            "email"
        ),
    )

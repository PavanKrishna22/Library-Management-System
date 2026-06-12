from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re


# =========================================================
# HELPERS
# =========================================================

def normalize_text(v: str | None):
    if not v:
        return None
    v = v.strip()
    v = " ".join(v.split())
    return v.title()


def normalize_email(v: str | None):
    if not v:
        return None
    v = v.strip().lower()
    return v


def normalize_phone(v: str | None):
    if not v:
        return None

    digits = re.sub(r"\D", "", v)

    if len(digits) == 10:
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    if len(digits) > 10:
        return "+" + digits

    return None


def parse_date(v: str | None):
    if not v:
        return None
    try:
        return datetime.strptime(v, "%Y-%m-%d").date()
    except Exception:
        return None


def validate_isbn(v: str | None):
    if not v:
        return None

    isbn = re.sub(r"[-\s]", "", v)

    if len(isbn) == 10 and isbn[:-1].isdigit():
        return isbn

    if len(isbn) == 13 and isbn.isdigit():
        return isbn

    return None


# =========================================================
# 📚 LIBRARY (STRICT)
# =========================================================

class Library(BaseModel):
    library_id: int
    name: str
    campus_location: str | None = None
    contact_email: EmailStr
    phone_number: str | None = None

    @field_validator("name", mode="before")
    @classmethod
    def name_check(cls, v):
        v = normalize_text(v)
        if not v:
            raise ValueError("Library name required")
        return v

    @field_validator("campus_location", mode="before")
    @classmethod
    def campus_clean(cls, v):
        return normalize_text(v)

    @field_validator("phone_number", mode="before")
    @classmethod
    def phone_clean(cls, v):
        return normalize_phone(v)


# =========================================================
# 📖 BOOK (STRICT)
# =========================================================

class Book(BaseModel):
    book_id: int
    title: str
    isbn: str
    publication_date: datetime | None = None
    total_copies: int | None = None
    available_copies: int | None = None
    library_id: int

    @field_validator("title", mode="before")
    @classmethod
    def title_check(cls, v):
        v = normalize_text(v)
        if not v:
            raise ValueError("Book title required")
        return v

    @field_validator("isbn", mode="before")
    @classmethod
    def isbn_check(cls, v):
        v = validate_isbn(v)
        if not v:
            raise ValueError("Invalid ISBN")
        return v

    @field_validator("publication_date", mode="before")
    @classmethod
    def date_check(cls, v):
        return parse_date(v)


# =========================================================
# ✍️ AUTHOR (STRICT)
# =========================================================

class Author(BaseModel):
    author_id: int
    first_name: str | None = None
    last_name: str
    birth_date: datetime | None = None
    nationality: str | None = None
    biography: str | None = None

    @field_validator("first_name", mode="before")
    @classmethod
    def first_clean(cls, v):
        return normalize_text(v)

    @field_validator("last_name", mode="before")
    @classmethod
    def last_check(cls, v):
        v = normalize_text(v)
        if not v:
            raise ValueError("Author last name required")
        return v

    @field_validator("birth_date", mode="before")
    @classmethod
    def birth_check(cls, v):
        return parse_date(v)


# =========================================================
# 👤 MEMBER (STRICT)
# =========================================================

class Member(BaseModel):
    member_id: int
    first_name: str | None = None
    last_name: str
    email: EmailStr
    phone: str | None = None
    member_type: str
    registration_date: datetime | None = None

    @field_validator("last_name", mode="before")
    @classmethod
    def last_check(cls, v):
        v = normalize_text(v)
        if not v:
            raise ValueError("Last name required")
        return v

    @field_validator("first_name", mode="before")
    @classmethod
    def first_clean(cls, v):
        return normalize_text(v)

    @field_validator("email", mode="before")
    @classmethod
    def email_clean(cls, v):
        v = normalize_email(v)
        if not v:
            raise ValueError("Email required")
        return v

    @field_validator("phone", mode="before")
    @classmethod
    def phone_clean(cls, v):
        return normalize_phone(v)

    @field_validator("registration_date", mode="before")
    @classmethod
    def date_clean(cls, v):
        return parse_date(v)
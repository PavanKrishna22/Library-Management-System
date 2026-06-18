from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Library(models.Model):
    library_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    campus_location = models.CharField(max_length=200)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "library"

    def __str__(self):
        return self.name


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    biography = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "author"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name
    

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    publication_date = models.DateField(null=True, blank=True)

    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book"

    def clean(self):
        if self.total_copies < 0:
            raise ValidationError(
                "Total copies cannot be negative."
            )

        if self.available_copies < 0:
            raise ValidationError(
                "Available copies cannot be negative."
            )

        if self.available_copies > self.total_copies:
            raise ValidationError(
                "Available copies cannot exceed total copies."
            )
    def is_available(self):
        return self.available_copies > 0

    def __str__(self):
        return self.title
    
    

class Member(models.Model):

    MEMBER_TYPES = [
        ("student", "Student"),
        ("faculty", "Faculty"),
    ]

    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    member_type = models.CharField(
        max_length=20,
        choices=MEMBER_TYPES
    )

    registration_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "member"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Borrowing(models.Model):
    borrowing_id = models.AutoField(primary_key=True)

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(
        null=True,
        blank=True
    )

    late_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "borrowing"

    def clean(self):
        if self.due_date < self.borrow_date:
            raise ValidationError(
                "Due date cannot be before borrow date."
            )

        if self.late_fee < 0:
            raise ValidationError(
                "Late fee cannot be negative."
            )
    
    def is_returned(self):
        return self.return_date is not None

    def is_overdue(self):
        if self.return_date:
            return False
        return timezone.now().date() > self.due_date


    def __str__(self):
        return f"{self.member} - {self.book}"



class Review(models.Model):
    review_id = models.AutoField(primary_key=True)

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField()

    comment = models.TextField(
        null=True,
        blank=True
    )

    review_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "review"
        unique_together = ("member", "book")
    
    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError(
                "Rating must be between 1 and 5."
            )
    
    def __str__(self):
        return f"{self.member} - {self.book}"
    


class BookAuthor(models.Model):
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookauthor"
        unique_together = ("book", "author")

    def __str__(self):
        return f"{self.book} - {self.author}"   


class BookCategory(models.Model):
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookcategory"
        unique_together = ("book", "category")

    def __str__(self):
        return f"{self.book} - {self.category}"


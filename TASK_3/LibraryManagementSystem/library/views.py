from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from django.db.models import Q, Sum

from django.db.models import Avg, Count

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
    inline_serializer,
)
from rest_framework import serializers

@extend_schema(
    summary="Health Check",
    description="""
Check whether the Library Management API is running.
""",
    tags=["System"]
)
@api_view(["GET"])
def health_check(request):
    return Response({
        "status": "success",
        "message": "Library Management API is running"
    })


@extend_schema(
    summary="Library Statistics",
    description="""
Returns overall statistics.

Example Response:

{
    "total_books":17,
    "total_members":25,
    "books_available":120,
    "books_borrowed":35
}
""",
    responses=inline_serializer(
        name="StatisticsResponse",
        fields={
            "total_libraries": serializers.IntegerField(),
            "total_books": serializers.IntegerField(),
            "total_authors": serializers.IntegerField(),
            "total_categories": serializers.IntegerField(),
            "total_members": serializers.IntegerField(),
            "total_borrowings": serializers.IntegerField(),
            "total_reviews": serializers.IntegerField(),
            "books_available": serializers.IntegerField(),
            "books_borrowed": serializers.IntegerField(),
        },
    ),
    tags=["Statistics"],
)
@api_view(["GET"])
def statistics(request):

    total_books = Book.objects.count()

    total_available = (
        Book.objects.aggregate(
            total=Sum("available_copies")
        )["total"] or 0
    )

    total_copies = (
        Book.objects.aggregate(
            total=Sum("total_copies")
        )["total"] or 0
    )

    return Response({

        "total_libraries":
            Library.objects.count(),

        "total_books":
            total_books,

        "total_authors":
            Author.objects.count(),

        "total_categories":
            Category.objects.count(),

        "total_members":
            Member.objects.count(),

        "total_borrowings":
            Borrowing.objects.count(),

        "total_reviews":
            Review.objects.count(),

        "books_available":
            total_available,

        "books_borrowed":
            total_copies - total_available,

    })

@extend_schema(
    tags=["Libraries"],
    summary="Library Management",
    description="""
CRUD operations for libraries.

Features:
- Create library
- View libraries
- Update library
- Delete library
"""
)
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all().order_by("library_id")
    serializer_class = LibrarySerializer

@extend_schema(
    tags=["Authors"],
    summary="Author Management",
    description="""
CRUD operations for authors.

Store author details including:
- Name
- Birth date
- Nationality
- Biography
"""
)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("author_id")
    serializer_class = AuthorSerializer


@extend_schema(
    tags=["Categories"],
    summary="Category Management",
    description="""
CRUD operations for book categories.

Examples:
- Fiction
- Mystery
- Fantasy
- Science
"""
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("category_id")
    serializer_class = CategorySerializer


@extend_schema(
    tags=["Books"],
    summary="Book Management",
    description="""
Manage books in the library.

Supports:

• CRUD operations

• Book search

• Book borrowing

• Book returns

• Book recommendations

• Availability checking

Filtering:
- library

Searching:
- title
- isbn

Ordering:
- title
- publication_date
- available_copies
"""
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("book_id")
    
    def get_serializer_class(self):

        if self.action in [
            "list",
            "retrieve",
            "search",
            "recommendations",
        ]:
            return NestedBookSerializer

        return BookSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "library",
    ]

    search_fields = [
        "title",
        "isbn",
    ]

    ordering_fields = [
        "title",
        "publication_date",
        "available_copies",
    ]

    @extend_schema(
        summary="Check Book Availability",
        description="""
    Returns:

    - Total copies
    - Available copies
    - Availability status
    """,
        tags=["Books"]
    )
    @action(detail=True, methods=["get"])
    def availability(self, request, pk=None):
        book = self.get_object()

        return Response({
            "book_id": book.book_id,
            "title": book.title,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies,
            "available": book.is_available()
        })

    @extend_schema(
        summary="Borrow Book",
        description="""
    Borrow a book.

    Required:

    {
        "member_id": 1,
        "book_id": 5
    }

    Automatically:
    - Creates borrowing record
    - Sets due date
    - Reduces available copies
    """,
        request=inline_serializer(
            name="BorrowBookRequest",
            fields={
                "member_id": serializers.IntegerField(),
                "book_id": serializers.IntegerField(),
            },
        ),
        responses={
            201: OpenApiResponse(
                description="Book borrowed successfully."
            ),
            400: OpenApiResponse(
                description="Invalid request."
            ),
        },
        tags=["Books"]
    )
    @action(detail=False, methods=["post"])
    def borrow(self, request):
        member_id = request.data.get("member_id")
        book_id = request.data.get("book_id")

        if not member_id or not book_id:
            return Response(
                {
                    "error": "member_id and book_id are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        member = get_object_or_404(
            Member,
            pk=member_id
        )

        book = get_object_or_404(
            Book,
            pk=book_id
        )

        if not book.is_available():
            return Response(
                {
                    "error": "Book is not available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        borrow_date = timezone.now().date()
        due_date = borrow_date + timedelta(days=7)

        borrowing = Borrowing.objects.create(
            member=member,
            book=book,
            borrow_date=borrow_date,
            due_date=due_date,
            return_date=None,
            late_fee=0
        )

        book.available_copies -= 1
        book.save()

        return Response(
            {
                "message": "Book borrowed successfully.",
                "borrowing_id": borrowing.borrowing_id,
                "member": member.member_id,
                "book": book.book_id,
                "borrow_date": borrowing.borrow_date,
                "due_date": borrowing.due_date,
                "available_copies": book.available_copies
            },
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Return Book",
        description="""
    Return a borrowed book.

    Required:

    {
        "borrowing_id": 10
    }

    Automatically:
    - Sets return date
    - Increases available copies
    """,
        request=inline_serializer(
            name="ReturnBookRequest",
            fields={
                "borrowing_id": serializers.IntegerField(),
            },
        ),
        responses={
            200: OpenApiResponse(
                description="Book returned successfully."
            ),
            400: OpenApiResponse(
                description="Invalid request."
            ),
        },
        tags=["Books"]
    )
    @action(detail=False, methods=["post"], url_path="return",
    url_name="return")
    def return_book(self, request):
        borrowing_id = request.data.get("borrowing_id")

        if not borrowing_id:
            return Response(
                {
                    "error": "borrowing_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing = get_object_or_404(
            Borrowing,
            pk=borrowing_id
        )

        if borrowing.is_returned():
            return Response(
                {
                    "error": "Book already returned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.return_date = timezone.now().date()
        borrowing.save()

        book = borrowing.book
        book.available_copies += 1
        book.save()

        return Response(
            {
                "message": "Book returned successfully.",
                "borrowing_id": borrowing.borrowing_id,
                "return_date": borrowing.return_date,
                "available_copies": book.available_copies
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Search Books",

        description="""
    Search books by:

    • Title
    • Author name
    • Category

    Example:

    /api/books/search/?search=Harry
    """,
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Search keyword",
            )
        ],
        tags=["Books"]
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        search = request.query_params.get("search")

        if not search:
            return Response(
                {
                    "error": "search parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ORM search for title
        title_ids = Book.objects.filter(
            title__icontains=search
        ).values_list(
            "book_id",
            flat=True
        )

        # SQL joins for author/category
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT b.book_id
                FROM book b

                LEFT JOIN bookauthor ba
                    ON b.book_id = ba.book_id
                LEFT JOIN author a
                    ON ba.author_id = a.author_id

                LEFT JOIN bookcategory bc
                    ON b.book_id = bc.book_id
                LEFT JOIN category c
                    ON bc.category_id = c.category_id

                WHERE
                    a.first_name ILIKE %s
                    OR a.last_name ILIKE %s
                    OR c.name ILIKE %s
                """,
                [
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%"
                ]
            )

            join_ids = [
                row[0]
                for row in cursor.fetchall()
            ]

        book_ids = set(title_ids) | set(join_ids)

        books = Book.objects.filter(
            book_id__in=book_ids
        ).order_by(
            "book_id"
        )

        serializer = self.get_serializer(
            books,
            many=True
        )

        return Response(serializer.data)
    

    @extend_schema(
        summary="Book Recommendations",
        description="""
    Recommend books based on borrowing history.

    Parameters:

    member_id
    limit

    If no borrowing history exists,
    top-rated available books are recommended.
    """,
        parameters=[
            OpenApiParameter(
                name="member_id",
                type=int,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Member ID",
            ),
            OpenApiParameter(
                name="limit",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Maximum recommendations",
            ),
        ],
        tags=["Books"]
    )
    @action(detail=False, methods=["get"])
    def recommendations(self, request):

        member_id = request.query_params.get("member_id")
        limit = request.query_params.get("limit", 3)

        try:
            limit = int(limit)
        except:
            limit = 3

        if limit < 1:
            limit = 3

        if limit > 10:
            limit = 10

        if not member_id:
            return Response(
                {
                    "error": "member_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        member = get_object_or_404(
            Member,
            pk=member_id
        )

        borrowed_books = Borrowing.objects.filter(
            member=member
        ).values_list(
            "book_id",
            flat=True
        )

        has_history = borrowed_books.exists()

        if has_history:

            borrowed_categories = BookCategory.objects.filter(
                book_id__in=borrowed_books
            ).values_list(
                "category_id",
                flat=True
            )

            books = Book.objects.filter(
                bookcategory__category_id__in=borrowed_categories,
                available_copies__gt=0
            ).exclude(
                book_id__in=borrowed_books
            ).annotate(
                average_rating=Avg(
                    "reviews__rating"
                ),
                borrow_count=Count(
                    "borrowings"
                )
            ).order_by(
                "-average_rating",
                "-borrow_count"
            ).distinct()

        else:

            books = Book.objects.filter(
                available_copies__gt=0
            ).annotate(
                average_rating=Avg(
                    "reviews__rating"
                ),
                borrow_count=Count(
                    "borrowings"
                )
            ).order_by(
                "-average_rating",
                "-borrow_count"
            )

        serializer = self.get_serializer(
            books[:limit],
            many=True
        )

        return Response(
            {
                "member_id": member.member_id,
                "recommendations": serializer.data
            }
        )


@extend_schema(
    tags=["Members"],
    summary="Member Management",
    description="""
CRUD operations for library members.

Supports:
- Student members
- Faculty members

Includes borrowing history endpoint.
"""
)
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by("member_id")
    serializer_class = MemberSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "member_type",
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]

    ordering_fields = [
        "first_name",
        "registration_date",
    ]

    @extend_schema(
        summary="Member Borrowing History",
        description="""
    Returns complete borrowing history for a member.
    """,
        responses=NestedBorrowingSerializer(many=True),
        tags=["Members"],
    )
    @action(detail=True, methods=["get"])
    def borrowings(self, request, pk=None):
        member = self.get_object()
        borrowings = Borrowing.objects.filter(
            member=member
        )

        serializer = NestedBorrowingSerializer(
            borrowings,
            many=True
        )

        return Response(serializer.data)



@extend_schema(
    tags=["Borrowings"],
    summary="Borrowing Management",
    description="""
CRUD operations for borrowings.

Stores:
- Borrow date
- Due date
- Return date
- Late fees
"""
)
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all().order_by("borrowing_id")
    
    def get_serializer_class(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            return NestedBorrowingSerializer

        return BorrowingSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "member",
        "book",
    ]

    search_fields = [
        "member__first_name",
        "member__last_name",
        "book__title",
    ]

    ordering_fields = [
        "borrow_date",
        "due_date",
        "late_fee",
    ]


@extend_schema(
    tags=["Reviews"],
    summary="Review Management",
    description="""
CRUD operations for book reviews.

Stores:
- Rating
- Comment
- Review date

One review per member per book.
"""
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("review_id")
    
    def get_serializer_class(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            return NestedReviewSerializer

        return ReviewSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "member",
        "book",
        "rating",
    ]

    search_fields = [
        "member__first_name",
        "member__last_name",
        "book__title",
        "comment",
    ]

    ordering_fields = [
        "rating",
        "review_date",
    ]


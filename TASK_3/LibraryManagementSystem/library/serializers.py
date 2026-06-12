from rest_framework import serializers
from .models import *


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


# ----------------------
# Nested Serializers
# ----------------------

class NestedBookSerializer(serializers.ModelSerializer):

    library = LibrarySerializer(read_only=True)

    authors = serializers.SerializerMethodField()

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_authors(self, obj):

        authors = Author.objects.filter(
            bookauthor__book=obj
        )

        return AuthorSerializer(
            authors,
            many=True
        ).data

    def get_categories(self, obj):

        categories = Category.objects.filter(
            bookcategory__book=obj
        )

        return CategorySerializer(
            categories,
            many=True
        ).data


class NestedBorrowingSerializer(serializers.ModelSerializer):

    member = MemberSerializer(
        read_only=True
    )

    book = NestedBookSerializer(
        read_only=True
    )

    class Meta:
        model = Borrowing
        fields = "__all__"


class NestedReviewSerializer(serializers.ModelSerializer):

    member = MemberSerializer(
        read_only=True
    )

    book = NestedBookSerializer(
        read_only=True
    )

    class Meta:
        model = Review
        fields = "__all__"
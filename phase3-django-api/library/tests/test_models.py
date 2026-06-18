from django.test import TestCase

from library.models import Library, Book


class LibraryModelTest(TestCase):

    def setUp(self):
        self.library = Library.objects.create(
            name="Central Library",
            campus_location="Block A",
            contact_email="central@gmail.com",
            phone_number="9999999999"
        )

    def test_create_library(self):

        self.assertEqual(
            self.library.name,
            "Central Library"
        )

    def test_library_string(self):

        self.assertEqual(
            str(self.library),
            "Central Library"
        )


class BookModelTest(TestCase):

    def setUp(self):

        self.library = Library.objects.create(
            name="Central",
            campus_location="A",
            contact_email="a@gmail.com",
            phone_number="1111111111"
        )

    def test_book_available(self):

        book = Book.objects.create(
            title="Python",
            isbn="123456789",
            total_copies=5,
            available_copies=3,
            library=self.library
        )

        self.assertTrue(
            book.is_available()
        )

    def test_book_not_available(self):

        book = Book.objects.create(
            title="Django",
            isbn="987654321",
            total_copies=2,
            available_copies=0,
            library=self.library
        )

        self.assertFalse(
            book.is_available()
        )

    def test_book_string(self):

        book = Book.objects.create(
            title="Machine Learning",
            isbn="111222333",
            total_copies=4,
            available_copies=4,
            library=self.library
        )

        self.assertEqual(
            str(book),
            "Machine Learning"
        )

    def test_book_total_equals_available(self):

        book = Book.objects.create(
            title="Data Science",
            isbn="444555666",
            total_copies=5,
            available_copies=5,
            library=self.library
        )

        self.assertTrue(
            book.is_available()
        )
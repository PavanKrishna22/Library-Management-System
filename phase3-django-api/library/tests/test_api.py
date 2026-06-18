from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Library


class LibraryAPITest(APITestCase):

    def setUp(self):

        # Create test user
        self.user = User.objects.create_superuser(
            username="admin",
            password="admin12345",
            email="admin@test.com"
        )

        # Login
        self.client.login(
            username="admin",
            password="admin12345"
        )

        # Create test library
        self.library = Library.objects.create(
            name="Central",
            campus_location="A Block",
            contact_email="central@gmail.com",
            phone_number="9999999999"
        )

    def test_health_check(self):

        response = self.client.get("/api/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_libraries(self):

        response = self.client.get(
            "/api/libraries/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_library(self):

        data = {
            "name": "North Library",
            "campus_location": "B Block",
            "contact_email": "north@gmail.com",
            "phone_number": "8888888888"
        }

        response = self.client.post(
            "/api/libraries/",
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_update_library(self):

        data = {
            "name": "Updated Library",
            "campus_location": "New Block",
            "contact_email": "central@gmail.com",
            "phone_number": "9999999999"
        }

        response = self.client.put(
            f"/api/libraries/{self.library.library_id}/",
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_library(self):

        response = self.client.delete(
            f"/api/libraries/{self.library.library_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_statistics(self):

        response = self.client.get(
            "/api/statistics/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_health_check(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)

    # -----------------------
    # Authors
    # -----------------------

    def test_get_authors(self):

        response = self.client.get(
            "/api/authors/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -----------------------
    # Categories
    # -----------------------

    def test_get_categories(self):

        response = self.client.get(
            "/api/categories/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -----------------------
    # Members
    # -----------------------

    def test_get_members(self):

        response = self.client.get(
            "/api/members/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -----------------------
    # Books
    # -----------------------

    def test_get_books(self):

        response = self.client.get(
            "/api/books/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -----------------------
    # Borrowings
    # -----------------------

    def test_get_borrowings(self):

        response = self.client.get(
            "/api/borrowings/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -----------------------
    # Reviews
    # -----------------------

    def test_get_reviews(self):

        response = self.client.get(
            "/api/reviews/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -----------------------
    # Book Search
    # -----------------------
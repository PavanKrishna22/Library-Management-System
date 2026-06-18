from django.test import TestCase

from library.serializers import LibrarySerializer


class LibrarySerializerTest(TestCase):

    def test_valid_serializer(self):

        data = {
            "name": "Central",
            "campus_location": "Block A",
            "contact_email": "test@gmail.com",
            "phone_number": "9999999999"
        }

        serializer = LibrarySerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):

        data = {
            "name": "",
            "campus_location": "",
            "contact_email": "bademail",
            "phone_number": ""
        }

        serializer = LibrarySerializer(data=data)

        self.assertFalse(serializer.is_valid())
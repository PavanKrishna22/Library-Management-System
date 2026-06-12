import logging
import time
import requests


class OpenLibraryClient:
    """
    Simple client for interacting with the Open Library API.
    """

    BASE_URL = "https://openlibrary.org"

    def __init__(self, delay: int = 1, timeout: int = 30):
        """
        Parameters:
            delay   : Seconds between API requests.
            timeout : HTTP request timeout.
        """
        self.delay = delay
        self.timeout = timeout

    def _make_request(self, endpoint: str):
        """
        Internal helper to make GET requests.
        """

        url = f"{self.BASE_URL}{endpoint}"

        try:
            logging.info("Requesting: %s", url)

            response = requests.get(
                url,
                timeout=self.timeout
            )

            response.raise_for_status()

            # Respect API rate limit
            time.sleep(self.delay)

            return response.json()

        except requests.exceptions.Timeout:
            logging.error("Request timed out: %s", url)

        except requests.exceptions.HTTPError as e:
            logging.error("HTTP error: %s", e)

        except requests.exceptions.ConnectionError:
            logging.error("Connection error.")

        except requests.exceptions.RequestException as e:
            logging.error("Request failed: %s", e)

        except Exception as e:
            logging.error("Unexpected error: %s", e)

        return None

    def search_author(self, author_name: str):
        """
        Search for an author.

        Example:
            search_author("Charles Dickens")
        """

        endpoint = f"/search/authors.json?q={author_name}"

        return self._make_request(endpoint)

    def get_author_works(self, author_key: str):
        """
        Fetch works by author.

        Input:
            OL24638A

        Endpoint:
            /authors/OL24638A/works.json
        """

        endpoint = f"/authors/{author_key}/works.json"

        return self._make_request(endpoint)

    def get_book_details(self, book_key: str):
        """
        Fetch book/edition details.

        Input:
            OL34720328M

        Endpoint:
            /books/OL34720328M.json
        """

        endpoint = f"/books/{book_key}.json"

        return self._make_request(endpoint)
    

    def get_work_details(self, work_key: str):
            """
            Fetch work details.

            Input:
                OL45804W

            Endpoint:
                /works/OL45804W.json
            """

            endpoint = f"/works/{work_key}.json"

            return self._make_request(endpoint)
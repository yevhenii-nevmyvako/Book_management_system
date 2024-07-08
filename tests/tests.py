import unittest
from httpx import AsyncClient
from fastapi import status

from main import app


class TestBookEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = AsyncClient(app=app, base_url="http://test")

    async def tearDown(self):
        await self.client.aclose()

    async def test_get_books_list(self):
        """Test should gets list of books"""
        response = await self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("books", response.text)

    async def test_create_book(self):
        """Should check creating the book."""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890123",
            "pages": 100
        }
        response = await self.client.post("/books/", json=book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Test Book")

    async def test_get_book_detail(self):
        """Should test book detail page."""
        create_response = await self.client.post("/books/", json={
            "title": "Test Book Detail",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890123",
            "pages": 100
        })
        book_id = create_response.json()['id']

        get_response = await self.client.get(f"/books/{book_id}")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.json()["title"], "Test Book Detail")

    async def test_update_book(self):
        """Should test updated the book."""
        create_response = await self.client.post("/books/", json={
            "title": "Test Book Update",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890123",
            "pages": 100
        })
        book_id = create_response.json()['id']

        update_response = await self.client.put(f"/books/{book_id}/update", json={
            "title": "Updated Test Book",
            "author": "Updated Author",
            "published_date": "2024-01-01",
            "isbn": "1234567890123",
            "pages": 150
        })
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.json()["title"], "Updated Test Book")

    async def test_delete_book(self):
        """Should test deleted the book."""
        create_response = await self.client.post("/books/", json={
            "title": "Test Book Delete",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890123",
            "pages": 100
        })
        book_id = create_response.json()['id']

        delete_response = await self.client.delete(f"/books/{book_id}")
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.json(), {"message": "Book deleted successfully"})


if __name__ == "__main__":
    unittest.main()

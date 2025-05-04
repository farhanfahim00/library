#By Sami Ul Haq & Farhan Fahim
#sami.haq@stud.th-deg.de
#farhan.taimoor@stud.th-deg.de

#All Imports
import unittest
from unittest.mock import patch, MagicMock
from library_main import add_book_gui, delete_book_gui, lend_book_gui, search_books_gui
from library_model import load_book


class TestLibraryIntegration(unittest.TestCase):
    """
    This is a simplified integration test.
    It checks if the key functions for adding, deleting, and lending books
    interact correctly with the model (data) and the view (UI).
    """

    # Test adding a book
    @patch('library_model.add_book')  # Mock the model's add_book function
    @patch('library_main.display_books')  # Mock the view's display_books function
    def test_add_book(self, mock_display_books, mock_add_book):
        # Simulate adding a book
        add_book_gui()

        # Check if add_book was called with the correct data
        mock_add_book.assert_called_with("Test Book", "Test Author", "2021", "available")

        # Check if display_books was called to update the view
        mock_display_books.assert_called()

    # Test deleting a book
    @patch('library_model.delete_book_by_title')  # Mock the model's delete function
    @patch('library_main.display_books')  # Mock the view's display_books function
    def test_delete_book(self, mock_display_books, mock_delete_book):
        # Simulate deleting a book
        delete_book_gui()

        # Check if delete_book_by_title was called with the correct book title
        mock_delete_book.assert_called_with("Test Book")

        # Check if display_books was called to update the view
        mock_display_books.assert_called()

    # Test lending a book
    @patch('library_model.save_books')  # Mock the model's save function
    @patch('library_model.load_book',
           return_value=[{'title': 'Test Book', 'status': 'available'}])  # Mock loading books
    @patch('library_main.display_books')  # Mock the view's display_books function
    def test_lend_book(self, mock_display_books, mock_load_books, mock_save_books):
        # Simulate lending a book
        lend_book_gui()

        # Check if save_books was called to update the book status
        mock_save_books.assert_called()

        # Check if display_books was called to update the view
        mock_display_books.assert_called()


if __name__ == '__main__':
    unittest.main()

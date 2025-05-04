#By Sami Ul Haq & Farhan Fahim
#sami.haq@stud.th-deg.de
#farhan.taimoor@stud.th-deg.de


#All Imports
import unittest
from unittest.mock import patch, MagicMock
from library_main import add_book_gui, delete_book_gui, lend_book_gui, search_books_gui, display_books
from library_model import load_book
#This is our complete System test checking the whole system works through checking the add and deletion capability

class TestLibrarySystem(unittest.TestCase):

    # Test for adding a book (Scenario 1)
    @patch('library_model.add_book')  # Mock the add_book function from the model
    @patch('library_main.display_books')  # Mock the display_books function
    @patch('tkinter.Entry')  # Mock Tkinter Entry widget
    def test_add_book(self, mock_entry, mock_display_books, mock_add_book):
        # Mock the behavior of Tkinter Entry widgets
        mock_entry.return_value.get.return_value = "Test Book"

        # Simulate the user adding a book
        add_book_gui()

        # Check that add_book was called with the correct parameters
        mock_add_book.assert_called_with("Test Book", "Test Author", "2021", "available")
        # Verify that the book list is updated after adding
        mock_display_books.assert_called()

    # Test for deleting a book (Scenario 2)
    @patch('library_model.delete_book_by_title')  # Mock the delete_book_by_title function
    @patch('library_main.display_books')  # Mock the display_books function
    @patch('tkinter.Entry')  # Mock Tkinter Entry widget
    def test_delete_book(self, mock_entry, mock_display_books, mock_delete_book):
        # Mock the behavior of Tkinter Entry widgets
        mock_entry.return_value.get.return_value = "Test Book"

        # Simulate the user deleting a book by title
        delete_book_gui()

        # Check that delete_book_by_title was called with the correct title
        mock_delete_book.assert_called_with("Test Book")
        # Verify that the book list is updated after deletion
        mock_display_books.assert_called()

    # Test for lending a book (Scenario 3)
    @patch('library_model.save_books')  # Mock the save_books function from the model
    @patch('library_model.load_book',
           return_value=[{'title': 'Test Book', 'status': 'available'}])  # Mock the load_book function
    @patch('library_main.display_books')  # Mock the display_books function
    @patch('tkinter.Entry')  # Mock Tkinter Entry widget
    def test_lend_book(self, mock_entry, mock_display_books, mock_load_books, mock_save_books):
        # Mock the behavior of Tkinter Entry widgets
        mock_entry.return_value.get.return_value = "Test Book"

        # Simulate the user lending a book
        lend_book_gui()

        # Verify that the book status was updated to "lent out"
        mock_save_books.assert_called()
        # Verify that the book list is updated after lending
        mock_display_books.assert_called()

    # Test for searching books (Scenario 4)
    @patch('library_model.load_book', return_value=[
        {'title': 'Test Book', 'author': 'Test Author', 'year': 2021, 'status': 'available'}])  # Mock load_book
    @patch('library_main.display_books')  # Mock the display_books function
    @patch('tkinter.Entry')  # Mock Tkinter Entry widget for search
    def test_search_books(self, mock_entry, mock_display_books, mock_load_books):
        # Mock the behavior of Tkinter Entry widgets
        mock_entry.return_value.get.return_value = "Test Book"

        # Simulate the user searching for a book
        search_books_gui()

        # Check that load_book was called to fetch the books
        mock_load_books.assert_called()
        # Verify that the search results are displayed
        mock_display_books.assert_called()

    # Test for displaying books (Scenario 5)
    @patch('library_model.load_book', return_value=[
        {'title': 'Test Book', 'author': 'Test Author', 'year': 2021, 'status': 'available'}])  # Mock load_book
    @patch('tkinter.Text')  # Mock Tkinter Text widget for displaying books
    def test_display_books(self, mock_text, mock_load_books):
        # Simulate displaying books
        mock_window = MagicMock()
        mock_text_area = MagicMock()
        display_books(mock_window, mock_text_area)

        # Check that the load_book was called to retrieve the books
        mock_load_books.assert_called()
        # Check that the book details are inserted into the text widget
        mock_text_area.insert.assert_called()


if __name__ == '__main__':
    unittest.main()

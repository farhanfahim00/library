# test_library_model.py
import unittest
from unittest.mock import patch, mock_open
from library_model import add_book, delete_book_by_title, load_book, save_books


class TestLibraryModel(unittest.TestCase):
#These are our unit tests where books are successfully added, loaded, deleted confirming all these functions

    # Test for adding a book
    @patch('builtins.open', new_callable=mock_open)
    def test_add_book(self, mock_file):
        # Add a book
        add_book("Test Book", "Test Author", 2021, "available")

        # Check if the file was opened in write mode
        mock_file.assert_called_with("library.json", 'w')


        # Check that the data being written to the file is correct
        mock_file.return_value.write.assert_called_with(
            '[{"title": "Test Book", "author": "Test Author", "year": 2021, "status": "available"}]\n')

        #book was successfully added


    # Test for loading books
    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"title": "Test Book", "author": "Test Author", "year": 2021, "status": "available"}]')
    def test_load_book(self, mock_file):
        # Load books and check the content
        books = load_book()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Test Book")

    # Test for deleting a book by title
    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"title": "Test Book", "author": "Test Author", "year": 2021, "status": "available"}]')
    def test_delete_book_by_title(self, mock_file):
        # Delete a book by title
        delete_book_by_title("Test Book")

        # Check if the file was opened in write mode and the content was updated correctly
        mock_file.assert_called_with("library.json", 'w')
        mock_file.return_value.write.assert_called_with(
            '[{"title": "Test Book", "author": "Test Author", "year": 2021, "status": "deleted"}]\n')

    # Test for saving books
    @patch('builtins.open', new_callable=mock_open)
    def test_save_books(self, mock_file):
        books = [{"title": "Test Book", "author": "Test Author", "year": 2021, "status": "available"}]
        save_books(books)

        # Check if the file was opened in write mode and data was written correctly
        mock_file.assert_called_with("library.json", 'w')
        mock_file.return_value.write.assert_called_with(
            '[{"title": "Test Book", "author": "Test Author", "year": 2021, "status": "available"}]\n')


if __name__ == '__main__':
    unittest.main()
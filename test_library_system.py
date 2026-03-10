"""
test_library_system.py

Automated tests for the Library Book Management System.

These tests check that the classes and functions behave correctly.

Run tests using:

pytest test_library_system.py -v
"""

import pytest
import os
import csv

from library_system import (
    Book,
    EBook,
    PrintedBook,
    Member,
    Library,
    save_books,
    load_books,
    save_members,
    load_members
)


# -----------------------------
# Base Book Class Tests
# -----------------------------

class TestBook:

    def test_create_book(self):

        book = Book("Python Basics", "John Smith", "Technology")

        assert book.title == "Python Basics"
        assert book.author == "John Smith"
        assert book.genre == "Technology"
        assert book.borrowed is False


    def test_book_str(self):

        book = Book("Python Basics", "John Smith", "Technology")

        assert str(book) == "Python Basics by John Smith (Technology) - Available"


    def test_missing_title(self):

        with pytest.raises(ValueError):
            Book("", "John Smith", "Technology")


    def test_invalid_genre(self):

        with pytest.raises(ValueError):
            Book("Book", "Author", "Cooking")


    def test_borrow_book(self):

        book = Book("Python Basics", "John Smith", "Technology")

        book.borrow()

        assert book.borrowed is True


    def test_return_book(self):

        book = Book("Python Basics", "John Smith", "Technology")

        book.borrow()
        book.return_book()

        assert book.borrowed is False
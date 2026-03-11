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

# -----------------------------
# EBook class tests
# -----------------------------

class TestEBook:

    def test_create_ebook(self):
        """Test creating an ebook."""

        ebook = EBook("AI Fundamentals", "Sarah Lee", "Technology", 5)

        assert ebook.title == "AI Fundamentals"
        assert ebook.author == "Sarah Lee"
        assert ebook.genre == "Technology"
        assert ebook.file_size == 5
        assert ebook.borrowed is False


    def test_ebook_string_output(self):
        """Test ebook string representation."""

        ebook = EBook("AI Fundamentals", "Sarah Lee", "Technology", 5)

        result = str(ebook)

        assert "AI Fundamentals" in result
        assert "EBook" in result


    def test_ebook_inherits_book(self):
        """EBook should inherit from Book."""

        ebook = EBook("AI Fundamentals", "Sarah Lee", "Technology", 5)

        assert isinstance(ebook, Book)

# -----------------------------
# PrintedBook class tests
# -----------------------------

class TestPrintedBook:

    def test_create_printed_book(self):
        """Test creating a printed book."""

        book = PrintedBook("World History", "Mark Johnson", "History", 400)

        assert book.title == "World History"
        assert book.pages == 400


    def test_printed_book_string_output(self):
        """Test printed book string representation."""

        book = PrintedBook("World History", "Mark Johnson", "History", 400)

        result = str(book)

        assert "World History" in result
        assert "pages" in result


    def test_printed_book_inherits_book(self):
        """PrintedBook should inherit from Book."""

        book = PrintedBook("World History", "Mark Johnson", "History", 400)

        assert isinstance(book, Book)

# -----------------------------
# Member class tests
# -----------------------------

class TestMember:

    def test_create_member(self):
        """Test creating a member."""

        member = Member("Alice", "alice@email.com")

        assert member.name == "Alice"
        assert member.email == "alice@email.com"
        assert member.borrowed_books == []


    def test_invalid_email(self):
        """Invalid email should raise ValueError."""

        with pytest.raises(ValueError):
            Member("Bob", "invalid-email")


    def test_borrow_book(self):
        """Member should be able to borrow a book."""

        member = Member("Alice", "alice@email.com")
        book = Book("Python Basics", "John Smith", "Technology")

        member.borrow_book(book)

        assert book.borrowed is True
        assert book in member.borrowed_books


    def test_return_book(self):
        """Member should be able to return a borrowed book."""

        member = Member("Alice", "alice@email.com")
        book = Book("Python Basics", "John Smith", "Technology")

        member.borrow_book(book)
        member.return_book(book)

        assert book.borrowed is False
        assert book not in member.borrowed_books

# -----------------------------
# Library class tests
# -----------------------------

class TestLibrary:

    def test_add_book(self):
        """Library should store books."""

        library = Library()
        book = Book("Python Basics", "John Smith", "Technology")

        library.add_book(book)

        assert book in library.books


    def test_register_member(self):
        """Library should store members."""

        library = Library()
        member = Member("Alice", "alice@email.com")

        library.register_member(member)

        assert member in library.members


    def test_find_book(self):
        """Library should find books by title."""

        library = Library()
        book = Book("Python Basics", "John Smith", "Technology")

        library.add_book(book)

        found = library.find_book("Python Basics")

        assert found == book


    def test_find_missing_book(self):
        """Searching for missing book should return None."""

        library = Library()

        result = library.find_book("Unknown Book")

        assert result is None

# -----------------------------
# CSV file saving tests
# -----------------------------

class TestCSVSave:

    def test_save_books(self):
        """Books should be saved to CSV."""

        library = Library()

        book = Book("Python Basics", "John Smith", "Technology")
        library.add_book(book)

        save_books(library)

        assert os.path.exists("books.csv")


    def test_save_members(self):
        """Members should be saved to CSV."""

        library = Library()

        member = Member("Alice", "alice@email.com")
        library.register_member(member)

        save_members(library)

        assert os.path.exists("members.csv")
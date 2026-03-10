"""
library_system.py
Library Book Management System

This project demonstrates key programming concepts:

- Object Oriented Programming (OOP)
- File Input/Output using CSV files
- Regular Expressions for validation
- External libraries
- Sorting with lambda functions
- Error handling

Run examples:

python3 library_system.py add
python3 library_system.py list
python3 library_system.py demo
"""

# -----------------------------
# Imports
# -----------------------------

import sys
import csv
import os
import re
import random

from faker import Faker


# -----------------------------
# Base Book Class
# -----------------------------

class Book:
    """
    Base class representing a book in the library.
    """

    VALID_GENRES = ["Fiction", "Science", "History", "Technology", "Education"]

    def __init__(self, title, author, genre):

        if not title:
            raise ValueError("Missing title")

        if not author:
            raise ValueError("Missing author")

        if genre not in Book.VALID_GENRES:
            raise ValueError("Invalid genre")

        self.title = title
        self.author = author
        self.genre = genre

        self.borrowed = False

    def borrow(self):
        """
        Mark book as borrowed.
        """

        if self.borrowed:
            raise ValueError("Book already borrowed")

        self.borrowed = True

    def return_book(self):
        """
        Return the book.
        """

        self.borrowed = False

    def __str__(self):
        status = "Borrowed" if self.borrowed else "Available"
        return f"{self.title} by {self.author} ({self.genre}) - {status}"

# -----------------------------
# Ebook Class (inherits Book)
# -----------------------------

class EBook(Book):
    """
    Represents a digital book.
    Inherits from the Book class.
    """

    def __init__(self, title, author, genre, file_size):
        super().__init__(title, author, genre)

        if file_size <= 0:
            raise ValueError("Invalid file size")

        self.file_size = file_size

    def download(self):
        """
        Simulate downloading the ebook.
        """
        return f"Downloading '{self.title}' ({self.file_size}MB)..."

    def __str__(self):
        return f"{self.title} by {self.author} [{self.genre}] (EBook {self.file_size}MB)"


# -----------------------------
# Printed Book Class
# -----------------------------

class PrintedBook(Book):
    """
    Represents a physical printed book.
    """

    def __init__(self, title, author, genre, pages):
        super().__init__(title, author, genre)

        if pages <= 0:
            raise ValueError("Invalid page number")

        self.pages = pages

    def __str__(self):
        return f"{self.title} by {self.author} [{self.genre}] ({self.pages} pages)"

# -----------------------------
# Member Class
# -----------------------------

class Member:
    """
    Represents a member of the library.
    Members can borrow and return books.
    """

    def __init__(self, name, email):

        if not name:
            raise ValueError("Missing name")

        # Regex email validation
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, email):
            raise ValueError("Invalid email")

        self.name = name
        self.email = email

        self.borrowed_books = []

    def borrow_book(self, book):
        """
        Borrow a book from the library.
        """

        if book.borrowed:
            raise ValueError("Book already borrowed")

        book.borrow()
        self.borrowed_books.append(book)

    def return_book(self, book):
        """
        Return a book to the library.
        """

        if book not in self.borrowed_books:
            raise ValueError("This member did not borrow this book")

        book.return_book()
        self.borrowed_books.remove(book)

    def __str__(self):
        return f"{self.name} ({self.email})"
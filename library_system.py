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

# -----------------------------
# Library Class
# -----------------------------

class Library:
    """
    Represents the library itself.
    It stores books and members and provides functions to manage them.
    """

    def __init__(self):

        self.books = []
        self.members = []

    def add_book(self, book):
        """
        Add a book to the library collection.
        """

        self.books.append(book)

    def register_member(self, member):
        """
        Register a new library member.
        """

        self.members.append(member)

    def list_books(self):
        """
        Print all books in the library sorted alphabetically.
        """

        if not self.books:
            print("No books in the library.")
            return

        for book in sorted(self.books, key=lambda b: b.title):
            print(book)

    def find_book(self, title):
        """
        Search for a book by title.
        """

        for book in self.books:
            if book.title.lower() == title.lower():
                return book

        return None

    def find_member(self, name):
        """
        Search for a member by name.
        """

        for member in self.members:
            if member.name.lower() == name.lower():
                return member

        return None

# -----------------------------
# File I/O Functions
# -----------------------------

def save_books(library):
    """
    Save all books in the library to a CSV file.
    """

    with open("books.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Type", "Title", "Author", "Genre", "Extra"])

        for book in library.books:

            if isinstance(book, EBook):
                writer.writerow(["ebook", book.title, book.author, book.genre, book.file_size])

            elif isinstance(book, PrintedBook):
                writer.writerow(["printed", book.title, book.author, book.genre, book.pages])


def load_books(library):
    """
    Load books from CSV file into the library.
    """

    if not os.path.exists("books.csv"):
        return

    with open("books.csv", "r") as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:

            book_type = row[0]
            title = row[1]
            author = row[2]
            genre = row[3]

            if book_type == "ebook":
                file_size = int(row[4])
                library.add_book(EBook(title, author, genre, file_size))

            elif book_type == "printed":
                pages = int(row[4])
                library.add_book(PrintedBook(title, author, genre, pages))


def save_members(library):
    """
    Save members to CSV.
    """

    with open("members.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Name", "Email"])

        for member in library.members:
            writer.writerow([member.name, member.email])


def load_members(library):
    """
    Load members from CSV.
    """

    if not os.path.exists("members.csv"):
        return

    with open("members.csv", "r") as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            name = row[0]
            email = row[1]

            library.register_member(Member(name, email))

# -----------------------------
# Fake Data Generator
# -----------------------------

def generate_demo_data(library):
    """
    Generate fake books and members using Faker.
    This helps demonstrate the system without manually typing data.
    """

    fake = Faker()

    genres = Book.VALID_GENRES

    # create random books
    for _ in range(5):

        title = fake.sentence(nb_words=3)
        author = fake.name()
        genre = random.choice(genres)

        if random.choice([True, False]):

            pages = random.randint(100, 600)
            book = PrintedBook(title, author, genre, pages)

        else:

            size = random.randint(1, 20)
            book = EBook(title, author, genre, size)

        library.add_book(book)

    # create random members
    for _ in range(3):

        name = fake.first_name()
        email = fake.email()

        member = Member(name, email)

        library.register_member(member)
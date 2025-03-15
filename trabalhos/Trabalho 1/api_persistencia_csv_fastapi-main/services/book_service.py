import csv
import os
import pandas as pd
from models.book import Book

CSV_FILE = 'books.csv'

class BookService:
    CSV_FILE = CSV_FILE

    @staticmethod
    def read_books():
        books = []
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            for _, row in df.iterrows():
                books.append(Book(**row.to_dict()))
        return books

    @staticmethod
    def write_books(books):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'title', 'author', 'year', 'genre', 'pages'])
            writer.writeheader()
            for book in books:
                writer.writerow(book.dict())

    @staticmethod
    def get_book(book_id: int):
        books = BookService.read_books()
        for book in books:
            if book.id == book_id:
                return book
        return None

    @staticmethod
    def create_book(book: Book):
        books = BookService.read_books()
        if any(b.id == book.id for b in books):
            return False
        books.append(book)
        BookService.write_books(books)
        return True

    @staticmethod
    def update_book(book_id: int, updated_book: Book):
        books = BookService.read_books()
        for i, book in enumerate(books):
            if book.id == book_id:
                books[i] = updated_book
                BookService.write_books(books)
                return updated_book
        return None

    @staticmethod
    def delete_book(book_id: int):
        books = BookService.read_books()
        for i, book in enumerate(books):
            if book.id == book_id:
                deleted_book = books.pop(i)
                BookService.write_books(books)
                return deleted_book
        return None
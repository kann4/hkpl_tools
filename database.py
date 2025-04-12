"""
1. insert book into database (book+book copies)
  a. insert book
  b. insert book copies
2. get available books (target library, unwanted libraries)
3. update all book copies
4. get last update date
5. get all saved books
6. delete saved books
"""

import sqlite3
from contextlib import contextmanager
import config
import data_model
from typing import List

@contextmanager
def get_db_connection(db_path=config.DB_PATH):
    connection = sqlite3.connect(db_path)
    try:
        yield connection
    finally:
        connection.close()


def insert_book(book: data_model.BookModel):
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement


def insert_book_copies(book_copies: List[data_model.BookCopyModel]):
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement


def get_available_books(
        library_name: str,
        libraries_to_remove: List[str]) -> List[data_model.BookCopyModel]:
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement


def update_book_copies(book_copies: List[data_model.BookCopyModel]):
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement


def get_last_update_date_str() -> str:
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement


def get_all_saved_books() -> List[data_model.BookModel]:
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement


def delete_books(books: List[data_model.BookModel]):
    with get_db_connection() as sqliteConnection:
        pass  # todo: implement

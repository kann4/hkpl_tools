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
        if connection:
            connection.close()
            print("The SQLite connection is closed")


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

def get_all_book_id_and_bib():
    with get_db_connection() as sqlite_connection:
        try:
            cursor = sqlite_connection.cursor()
            sqlite_select_query = """SELECT bookID, bibID from Book ORDER BY bookID"""
            cursor.execute(sqlite_select_query)
            bookID_bibID = cursor.fetchall(
            )  #running cursor.fetchall twice will fetch nothing in second time
            return bookID_bibID
        except sqlite3.Error as error:
            print('**************failed to get bookID and bibID from Book table, error: ', error,
              '**************************')

def update_book_copies_by_book_id_and_bib(bookID_bibID):
    with get_db_connection() as sqlite_connection:
        cursor = sqlite_connection.cursor()
        for book_ID, bib in bookID_bibID:  # for item in <expression>:
            try:
                sqlite_delete_query = "DELETE FROM BookCopy WHERE bookID = ?"
                cursor.execute(sqlite_delete_query, (book_ID, ))
                copies = get_info(bib, get_book_info=False)
                # print(f'****copies****{copies}**********')
                insertCopies(book_ID, copies, cursor)
                sqliteConnection.commit()
                print(
                    f'*************{book_ID} is updated successfully*************'
                )
            except sqlite3.Error as error:
                print(
                    f'***************Failed to update {book_ID}/{bib}, {error}********************'
                )
                books_failed_to_update.append((book_ID, bib))
            cursor.close()


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

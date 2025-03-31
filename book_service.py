"""
1. add book by bib or url
  a. add book by bib
  b. add book by url
2. get available books (target library, unwanted libraries)
3. update all book copies
4. get last update date
5. get all saved books
6. delete saved book
7. search books on hkpl by search_term
"""
from original_src.db import getBookTable as db_getBookTable, delBook as db_delBook

def getBookTable():
    return db_getBookTable()

def delBook(book_ids):
    return db_delBook(book_ids)
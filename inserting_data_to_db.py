import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from beautifulsoup_testing import get_info

def insertIntoTables(bib):
    info = get_info(bib)
    book = info[0]
    copies = info[1]
    try:
        sqliteConnection = sqlite3.connect('hkpl_tools.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query_book = """INSERT INTO Book
                          (bookName, author, bibID, callNumber, physicalDescription,placeOfPublication, publisher,
                           publicationYear, seriesTitle, subject, addedAuthor, standardNumber, language, creationDate, lastUpdateDate) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        #sqlite_insert_query_bookcopy = """INSERT INTO BookCopy
        #                  (bookID, libraryID, status, dueDate, collection, creationDate, lastUpdateDate) 
        #                  VALUES (?, ?, ?, ?, ?, ?, ?);"""

        cursor.execute(sqlite_insert_query_book, book)
        bookID = cursor.lastrowid
        for copy in copies:
            copy.insert(0,bookID)
        #for copy in copies:
        #    cursor.execute(sqlite_insert_query_bookcopy, copy)
        sqliteConnection.commit()
        print("inserted successfully into sqlite table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

bib = 147569
insertIntoTables(bib)

import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from beautifulsoup_testing import get_info
    
def insertIntoTables(bib):
    info = get_info(bib.lstrip('0'))
    book = info[0]
    copies = info[1]
    try:
        sqliteConnection = sqlite3.connect('hkpl_tools.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = """INSERT INTO Book
                          (bookName, author, bibID, callNumber, physicalDescription,placeOfPublication, publisher,
                           publicationYear, seriesTitle, subject, addedAuthor, standardNumber, language, creationDate, lastUpdateDate) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(sqlite_insert_query, book)
        cursor.execute("SELECT bookID FROM Book ORDER BY bookID DESC LIMIT 1")
        book_ID = cursor.fetchone()[0]

        for copy in copies:
            copy.insert(0,book_ID)
            sqlite_select_query = """SELECT libraryID from Library where englishName = ?"""
            cursor.execute(sqlite_select_query, (copy[1],))
            library_ID = cursor.fetchone()[0]
            copy[1] = library_ID
            if copy[2][:3] == 'Due':
                due_date = copy[2][4:]
            else:
                due_date = 'NA'
            copy.insert(3,due_date)
        sqlite_insert_query_bookcopy = """INSERT INTO BookCopy
                          (bookID, libraryID, status, dueDate, collection, creationDate, lastUpdateDate) 
                          VALUES (?, ?, ?, ?, ?, ?, ?);"""
        for copy in copies:
            cursor.execute(sqlite_insert_query_bookcopy, copy)
            
        sqliteConnection.commit()
        print("Data of " + str(bib) +" is inserted successfully into sqlite db")
        cursor.close()

    except sqlite3.Error as error:
        if str(error) == 'UNIQUE constraint failed: Book.standardNumber':
            print(f'{bib} ({book[0]}) is already in the database.')
        else:
            print("Failed to insert into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

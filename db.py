import sqlite3
from beautifulsoup import get_info
import config

def get_db_connection():
    return sqlite3.connect(config.DB_PATH)

def insertIntoTables(bib):
    info = get_info(bib)
    if type(info) is str:
        return info                 # type(info) is str if error occur during getting book info. Return value of get_info() will be the error msg.
    book = info[0]
    copies = info[1]
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite, insert new entry.")

        sqlite_insert_query = """INSERT INTO Book
                          (bookName, author, bibID, callNumber, physicalDescription,placeOfPublication, publisher,
                           publicationYear, seriesTitle, subject, addedAuthor, standardNumber, language, creationDate, lastUpdateDate) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(sqlite_insert_query, book)
        cursor.execute("SELECT bookID FROM Book ORDER BY bookID DESC LIMIT 1")
        book_ID = cursor.fetchone()[0]

        insertCopies(book_ID,copies,cursor)
        sqliteConnection.commit()
        cursor.close()
        msg = f"{book[0]} / {bib} is added successfully into the database"
        print(msg)
        return msg

    except sqlite3.Error as error:
        if str(error) == 'UNIQUE constraint failed: Book.standardNumber':
            msg = f'{bib} ({book[0]}) is already in the database. (error: UNIQUE constraint failed: Book.standardNumber)'
            print(msg)
            return msg
        elif str(error) == 'UNIQUE constraint failed: Book.bibID':   #which error?
            msg = f'{bib} "{book[0]}" is already in the database. (error: UNIQUE constraint failed: Book.bibID)'
            print(msg)
            return msg
        else:
            msg = f"Failed to insert into sqlite table {error}"
            print(msg)
            return msg
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getCopies(library_name):   #get copies availabe in certain libraary
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite, getting copies from db...")

        library_ID = getLibraryID(cursor, library_name)
        sqlite_select_query = """SELECT bookID, status, collection from bookCopy where libraryID = ?"""
        cursor.execute(sqlite_select_query, (library_ID,))
        copies = cursor.fetchall()
        copies = [list(elem) for elem in copies]
        for copy in copies:
            sqlite_select_query = """SELECT bookName, callNumber from Book where bookID = ?"""
            cursor.execute(sqlite_select_query, (copy[0],))
            x = cursor.fetchone()
            copy[0] = x[0]
            copy.insert(1,x[1])
        return copies
    except sqlite3.Error as error:
        print('**************failed to get copies', error,'**************************')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def updateCopies():
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite: Begin to update copies...")
        
        sqlite_select_query = """SELECT bookID, bibID from Book ORDER BY bookID"""
        cursor.execute(sqlite_select_query)
        books_failed_to_update = []
        bookID_bibID = cursor.fetchall()          #running cursor.fetchall twice will fetch nothing in second time
        for book_ID, bib in bookID_bibID :      # for item in <expression>:      
            try:
                sqlite_delete_query = "DELETE FROM BookCopy WHERE bookID = ?" 
                cursor.execute(sqlite_delete_query,(book_ID,))
                copies = get_info(bib, get_book_info=False)
                # print(f'****copies****{copies}**********')
                insertCopies(book_ID,copies,cursor)
                sqliteConnection.commit()
                print(f'*************{book_ID} is updated successfully*************')
            except sqlite3.Error as error:
                print(f'***************Failed to update {book_ID}/{bib}, {error}********************')
                books_failed_to_update.append((book_ID, bib))

        cursor.close()
        return books_failed_to_update           

    except sqlite3.Error as error:
        print('**************update process failed', error,'**************************')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def insertCopies(book_ID,copies,cursor):      #contain query code only, use for insertIntoTables() and updateCopies()
    for copy in copies:
        copy.insert(0,book_ID)
        library_ID = getLibraryID(cursor, copy[1])
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

def getLibraryID(cursor, library_name):
    sqlite_select_query = """SELECT libraryID from Library where englishName = ?"""
    cursor.execute(sqlite_select_query, (library_name,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError(f"Library with name '{library_name}' not found.")
    library_ID = result[0]
    return library_ID

def lastUpdate():
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite, start get last update time")

        sqlite_select_query = """SELECT lastUpdateDate from BookCopy ORDER BY lastUpdateDate DESC LIMIT 1"""
        cursor.execute(sqlite_select_query)
        result = cursor.fetchone()
        if result:
            lastupdate = result[0]
        else:
            lastupdate = None  # or raise an exception
        return lastupdate

    except sqlite3.Error as error:
        print('**************cannot get lastupdate time', error,'**************************')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getBookTable():
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        cursor.execute("SELECT * from Book")
        books = cursor.fetchall()
        # print(books)
        cursor.execute("PRAGMA table_info(Book)")
        table_info = cursor.fetchall()
        column_names = [tup[1] for tup in table_info]       #list comprehension 
        # print(column_names)
        return column_names, books
    except sqlite3.Error as error:
        print('**************failed to get books', error,'**************************')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def listOfLibraries():
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite: getting list of libraries")
        cursor.execute("SELECT englishName, libraryNumber from Library ORDER BY libraryID ASC")
        results = cursor.fetchall()
        # print(results)
        libraries = [{'englishName': result[0], 'libraryNumber': result[1]} for result in results]
        return libraries
    except sqlite3.Error as error:
        print('**************failed to get list of libraries', error,'**************************')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
def delBook(book_IDs):
    try:
        sqliteConnection = get_db_connection()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        for book_ID in book_IDs:
            cursor.execute("DELETE from Book WHERE bookID = ?", (book_ID,))
            cursor.execute("DELETE from BookCopy WHERE bookID = ?", (book_ID,))
        sqliteConnection.commit()
        cursor.close()
        return book_IDs
    except sqlite3.Error as error:
        print('**************failed to delete', error,'**************************')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

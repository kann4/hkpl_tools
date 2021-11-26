import sqlite3
import urllib.request
from bs4 import BeautifulSoup

#config
bib = 3563388
#locale = 'en'
locale = 'zh_TW'

def get_value(book_info_type):
    
    book_info = table_book_info.find('td', string=book_info_type).find_next_sibling('td').string
    if book_info == None:
        divs = table_book_info.find('td', string=book_info_type).find_next_sibling('td').find_all('div')
        book_info = divs[0].string + '\n ' + divs[1].string
    return book_info

def insertIntoTables(book,copies):
    try:
        sqliteConnection = sqlite3.connect('hkpl_tools.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query_book = """INSERT INTO Book
                          (bookName, author, bibID, callNumber, physicalDescription,placeOfPublication, publisher,
                           publicationYear, seriesTitle, subject, addedAuthor, standardNumber, language, creationDate, lastUpdateDate) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        sqlite_insert_query_bookcopy = """INSERT INTO BookCopy
                          (id, name, email, joining_date, salary) 
                          VALUES (?, ?, ?, ?, ?);"""

        cursor.execute(sqlite_insert_query_book, book)
        for copy in copies:
            cursor.execute(sqlite_insert_query_bookcopy, copy)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def main():
    url = 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:'+str(bib)+'&fromLocationLink=false&theme=mobile&showAll=true&locale='+locale
    response = urllib.request.urlopen(url)
    htmlbytes = response.read()
    bs = BeautifulSoup(htmlbytes, "html.parser")
    
    #get book info  
    table_book_info = bs.find('div', class_='itemFields').table     #need to run this line before get_value()
    items_to_get = [Author, ]
    book = ()
    book_title = bs.find('h1', class_='title').string
    book.append(book_title)
    for x in items_to_get:
        book.append(get_value(x))
    
    book.append()
    #get book copies
    table_copies = bs.find_all('form')[2].tbody
    trs = table_copies.find_all('tr')[:-1]
    copies=[]
    for i in range(len(trs)):
        copies.append([])    
    i = 0
    for tr in trs:
        tds = tr.find_all('div')
        copy_name = tds[0].string
        status = tds[3].string
        collection = tds[4].string
        copies[i] = [copy_name,status,collection]
        i += 1

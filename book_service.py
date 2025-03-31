"""
1. add book by bib or url
  a. add book by bib
  b. add book by url
2. get available books (target library, unwanted libraries)
3. update all book copies
4. get last update date
5. get all saved books
6. delete saved book
7. get list of libraries
"""
from urllib.parse import urlparse, parse_qs
from original_src.db import getBookTable as db_getBookTable, delBook as db_delBook, \
  insertIntoTables, updateCopies as db_updateCopies, lastUpdate as db_lastUpdate, listOfLibraries as db_listOfLibraries, getCopies as db_getCopies

def convert_to_bib(bib_or_url):
    # Try Parse bib as URL
    parsed_url = urlparse(bib_or_url)
    query_params = parse_qs(parsed_url.query) # Extract the query string
    id_value = query_params.get('id', [None])[0] # Get the 'id' parameter: should be in format "chamo:3655993"
    id = id_value.split(':')[-1] if id_value else None # Extract the numeric part after the colon)
    # End of parsing bib as URL
    bib = id if id else bib_or_url # Use the extracted ID if available, otherwise use the original bib value
    return bib

def add_book_by_bib_or_url(bib_or_url):
    bib = convert_to_bib(bib_or_url) # Convert the input to bib
    print(bib) # Print the final bib value to be used
    message = insertIntoTables(bib)
    return message

def getCopies(target_library, unwanted_libraries):
   return db_getCopies(target_library, unwanted_libraries)

def updateCopies():
    return db_updateCopies()

def lastUpdate():
    return db_lastUpdate()

def getBookTable():
    return db_getBookTable()

def delBook(book_ids):
    return db_delBook(book_ids)

def listOfLibraries():
    return db_listOfLibraries()
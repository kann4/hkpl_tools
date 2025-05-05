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
from original_src.db import (
    getBookTable as db_getBookTable,
    delBook as db_delBook,
    insertIntoTables,
    updateCopies as db_updateCopies,
    lastUpdate as db_lastUpdate,
    listOfLibraries as db_listOfLibraries,
    getCopies as db_getCopies,
    get_all_book_id_and_bib_id,
)
from hkpl_service import get_url_from_bib, get_htmlbytes, get_book_info, get_copies_info


def convert_to_bib(bib_or_url):
    # Try Parse bib as URL
    parsed_url = urlparse(bib_or_url)
    query_params = parse_qs(parsed_url.query)  # Extract the query string
    id_value = query_params.get('id', [None])[
        0
    ]  # Get the 'id' parameter: should be in format "chamo:3655993"
    _id = (
        id_value.split(':')[-1] if id_value else None
    )  # Extract the numeric part after the colon)
    # End of parsing bib as URL
    bib = (
        _id if _id else bib_or_url
    )  # Use the extracted ID if available, otherwise use the original bib value
    return bib


def add_book_by_bib_or_url(bib_or_url):
    bib = convert_to_bib(bib_or_url)  # Convert the input to bib
    print(bib)  # Print the final bib value to be used
    url = get_url_from_bib(bib)
    bs = get_htmlbytes(url)
    if type(bs) is str:
        return bs  # bs is the error msg if url cannot reach
    book = get_book_info(bs)
    copies = get_copies_info(bs)
    message = insertIntoTables(book, copies)
    return message


def get_copies(target_library, unwanted_libraries):
    return db_getCopies(target_library, unwanted_libraries)


def update_all_copies():
    bookID_bibID = get_all_book_id_and_bib_id()
    return db_updateCopies(bookID_bibID)


def update_current_copies(target_library, unwanted_libraries):
    bookID_bibID = [
        (copies[4], copies[5])
        for copies in get_copies(target_library, unwanted_libraries)
    ]  # remove unused columns from copies
    unique = list(set(bookID_bibID))
    # print(bookID_bibID) # Print the list of bookID and bibID pairs to be updated
    return db_updateCopies(unique)


def get_last_update():
    return db_lastUpdate()


def get_book_table():
    return db_getBookTable()


def del_book(book_ids):
    return db_delBook(book_ids)


def get_list_of_libraries():
    return db_listOfLibraries()

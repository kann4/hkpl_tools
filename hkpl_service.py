"""
1. get book info and copy info
  a. get by bib
  b. get by url
2. search books by search_term
"""

import urllib.request
import urllib.error
import datetime
from bs4 import BeautifulSoup


def get_url_from_bib(bib: str):
    """
    Return the url of a book given its bib id.

    :param bib: book id
    :type bib: str
    :return: url of the book
    :rtype: str
    """
    return 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:' \
    + str(bib).lstrip('0') \
    + '&fromLocationLink=false&theme=mobile&showAll=true&locale=en'


def get_htmlbytes(bib_or_url: str):
    """
    Return a BeautifulSoup object given a book id or url.

    :param bibOrUrl: book id or url
    :type bibOrUrl: str
    :return: parsed html of the book's page
    :rtype: BeautifulSoup
    """
    if bib_or_url.startswith('https://webcat.hkpl.gov.hk'):
        url = bib_or_url
    else:
        url = get_url_from_bib(bib_or_url)
    try:
        response = urllib.request.urlopen(
            urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    except urllib.request.HTTPError as e:
        print(e)
        return f'Error. "{url}" cannot be reached. Check hkpl web or bib exist.'

    htmlbytes = response.read()
    bs = BeautifulSoup(htmlbytes, "html.parser")
    return bs


def get_book_info(bs: BeautifulSoup):
    """
    Extracts book information from a BeautifulSoup object and returns it as a tuple.

    The function retrieves the book title and various bibliographic details 
    from the parsed HTML content of a webpage. It also includes the current 
    date twice at the end of the returned tuple.

    :param bs: A BeautifulSoup object representing the parsed HTML content of a book's webpage.
    :type bs: BeautifulSoup
    :return: A tuple containing the book title, bibliographic details, and two current date entries.
    :rtype: tuple
    """

    today_date = datetime.date.today()
    book = []
    book_title = bs.find('h1', class_='title').string
    book.append(book_title)

    items = [
        'Author', 'Bib ID', 'Call Number', 'Physical Description',
        'Place of Publication', 'Publisher', 'Year', 'Series Title', 'Subject',
        'Added Author', 'Standard No.', 'Language'
    ]

    table_book = bs.find('div', class_='itemFields').table
    for item in items:
        book.append(get_value(table_book, item))
    book.append(str(today_date))
    book.append(str(today_date))
    tuple(book)
    return book


def get_value(table_book, book_info_type, table_found=[False]):
    """
    Retrieves the value of a book information type from a parsed HTML content of a book's webpage.

    The function takes a parsed HTML content of a book's webpage and the type of book information 
    to retrieve as parameters. It returns the value of the specified book information type 
    as a string. If the information type is not found, it returns 'N/A'.

    :param table_book: A BeautifulSoup object representing the parsed HTML content of a book's webpage.
    :type table_book: BeautifulSoup
    :param book_info_type: The type of book information to retrieve.
    :type book_info_type: str
    :return: The value of the specified book information type as a string.
    :rtype: str
    """
    td = table_book.find('td', string=book_info_type)     #tdre where item name is placed
    if td != None:
        book_info = td.find_next_sibling('td').string      #next td is the value of the item
        if book_info == None:                               #sometimes the info has > 1 line. td is empty. Those info are placed in the divs inside that td
            book_info = ''
            divs = td.find_next_sibling('td').find_all('div')
            for div in divs:
                book_info = book_info + div.string + '\n'
    else:
        return 'N/A'
    return book_info


def get_copy_info(bs: BeautifulSoup):
    """
    Extracts copy information from a BeautifulSoup object and returns it as a list of lists.

    The function retrieves the library name, status, collection, creation date, and last update date 
    for each copy of a book from the parsed HTML content of a webpage.
    
    :param bs: A BeautifulSoup object representing the parsed HTML content of a book's webpage.
    :type bs: BeautifulSoup
    :return: A list of lists, each containing the library name, status, collection, creation date, and last update date for a copy of a book.
    :rtype: list
    """
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table_copies = bs.find_all('form')[2].tbody
    trs = table_copies.find_all('tr')[:-1]
    copies = []
    for i in range(len(trs)):
        copies.append([])
    for i in range(len(trs)):
        divs = trs[i].find_all('div')
        library = divs[0].string[4:].rstrip()
        status = divs[3].string
        collection = divs[4].string
        creation_date = last_update_date = str(time_now)
        copies[i] = [
            library, status, collection, creation_date, last_update_date
        ]
    return copies

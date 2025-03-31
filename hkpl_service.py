"""
1. get book info and copy info
  a. get by bib
  b. get by url
2. search books by search_term
TODO: use dataclass to replace dictionary
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


def get_value(table_book, book_info_type):
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
    td = table_book.find(
        'td', string=book_info_type)  #tdre where item name is placed
    if td is not None:
        book_info = td.find_next_sibling(
            'td').string  #next td is the value of the item
        if book_info is None:  #sometimes the info has > 1 line. td is empty. Those info are placed in the divs inside that td
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
    for i, tr in enumerate(trs):
        divs = tr.find_all('div')
        library = divs[0].string[4:].rstrip()
        status = divs[3].string
        collection = divs[4].string
        creation_date = last_update_date = str(time_now)
        copies[i] = [
            library, status, collection, creation_date, last_update_date
        ]
    return copies


def get_search_url(search_term):
    url_template = 'https://webcat.hkpl.gov.hk/search/query?term_1={search_term}&theme=WEB&locale=en'
    return url_template.format(search_term=urllib.parse.quote(search_term))


def get_book_list(search_term):
    url = get_search_url(search_term)
    try:
        response = urllib.request.urlopen(
            urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    except urllib.request.HTTPError as e:
        print(e)
        return f'Error. "{url}" cannot be reached. Check hkpl web or bib exist.'

    htmlbytes = response.read()
    bs = BeautifulSoup(htmlbytes, "html.parser")
    books = []

    # Extract book information
    records = bs.find_all('li', class_='record')
    for record in records:
        book_info = {}
        record_highlight = record.find('div', class_='recordHighlight')
        if record_highlight:
            # Extract publication and call number
            item_fields = record_highlight.find('div', class_='itemFields')

            # Extract image URL
            img_tag = record.find('div', class_='recordImage').find('img')
            if img_tag and img_tag.get('src'):
                book_info['image_url'] = img_tag['src']

            if item_fields:
                for row in item_fields.find_all('tr'):
                    label = row.find('td', class_='label')
                    if label and label.text.strip() == 'Publication':
                        book_info['publication'] = label.find_next_sibling(
                            'td').text.strip()
                    if label and label.text.strip() == 'Call Number':
                        book_info['call_number'] = label.find_next_sibling(
                            'td').text.strip()

            # Extract availability
            availability = record.find('span', class_='availabilityTotal')
            if availability:
                availability_text = availability.text.strip()
                try:
                    book_info['available_copies'] = int(
                        availability_text.split()[0])
                except (ValueError, IndexError):
                    book_info['available_copies'] = 0

            # Extract title and ID
            title = record_highlight.find('a', class_='title')
            if title:
                book_info['title'] = title.text.strip()
                # Extract ID from href
                href = title.get('href')
                if href:
                    book_info['bib'] = href.split('id=')[1].split(
                        '&')[0].split(':')[1] if 'id=' in href else None

            if book_info:  # Only add if we have complete information
                books.append(book_info)

    # write bs.contents to file
    # with open('output.html', 'w', encoding='utf-8') as f:
    #     f.write(str(bs.contents))# print(bs.prettify())  # This will print the prettified HTML to the console
    # You can also write the prettified HTML to a file if needed
    # with open('output_prettified.html', 'w', encoding='utf-8') as f:
    #     f.write(bs.prettify())  # This will write the prettified HTML to a file
    return books

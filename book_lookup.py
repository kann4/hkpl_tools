import urllib.request
from bs4 import BeautifulSoup
import urllib.parse

url_template = 'https://webcat.hkpl.gov.hk/search/query?term_1={search_term}&theme=WEB&locale=en'

def get_search_url(search_term):
    return url_template.format(search_term=urllib.parse.quote(search_term))

def get_book_list(search_term):
    url = get_search_url(search_term)
    try:
        response = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}))
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
            if item_fields:
                for row in item_fields.find_all('tr'):
                    label = row.find('td', class_='label')
                    if label and label.text.strip() == 'Publication':
                        book_info['publication'] = label.find_next_sibling('td').text.strip()
                    if label and label.text.strip() == 'Call Number':
                        book_info['call_number'] = label.find_next_sibling('td').text.strip()
            
            # Extract title and ID
            title = record_highlight.find('a', class_='title')
            if title:
                book_info['title'] = title.text.strip()
                # Extract ID from href
                href = title.get('href')
                if href:
                    book_info['id'] = href.split('id=')[1].split('&')[0].split(':')[1] if 'id=' in href else None
            
            if book_info:  # Only add if we have complete information
                books.append(book_info)
            
    # write bs.contents to file
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(str(bs.contents))# print(bs.prettify())  # This will print the prettified HTML to the console
    # You can also write the prettified HTML to a file if needed
    with open('output_prettified.html', 'w', encoding='utf-8') as f:
        f.write(bs.prettify())  # This will write the prettified HTML to a file
    return books

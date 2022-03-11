import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import datetime

def get_info(bib):
    global book, copies
    def get_value(book_info_type, table_found=[False]):
        global table_book
        if table_found == [False]:
            table_book = bs.find('div', class_='itemFields').table          
            table_found[0] = True
        td = table_book.find('td', string=book_info_type)     #td where item name is placed
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

    url = 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:'+str(bib)+'&fromLocationLink=false&theme=mobile&showAll=true&locale=en'
    # response = urllib.request.urlopen(url)
    try:
        response = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}))
    except urllib.request.HTTPError as e:
        print(e)
        return

    htmlbytes = response.read()
    bs = BeautifulSoup(htmlbytes, "html.parser")
    today_date = datetime.date.today()
    #book
    book = []
    book_title = bs.find('h1', class_='title').string
    book.append(book_title)
    
    items = ['Author', 'Bib ID', 'Call Number', 'Physical Description', 'Place of Publication', 'Publisher',
    'Year', 'Series Title', 'Subject', 'Added Author', 'Standard No.', 'Language']
    for item in items:
        book.append(get_value(item))
    book.append(str(today_date))
    book.append(str(today_date))
    tuple(book)
    #copies
    table_copies = bs.find_all('form')[2].tbody
    trs = table_copies.find_all('tr')[:-1]
    copies=[]
    for i in range(len(trs)):
        copies.append([])    
    for i in range(len(trs)):
        divs = trs[i].find_all('div')
        library = divs[0].string[4:].rstrip()
        status = divs[3].string
        collection = divs[4].string
        creation_date =  last_update_date = str(today_date)
        copies[i] = [library,status,collection,creation_date,last_update_date]    

    return (book,copies)

# print(get_info(003563388))
# print(len(copies))    

#why has to put get_value() inside?
#why 58-60 is runned?

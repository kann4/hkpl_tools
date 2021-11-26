import urllib.request
from bs4 import BeautifulSoup
import datetime

#testing Bib
#2835575
#3632431
#3563388 /snowden

""" #config
bib = 3563388
locale = 'en'
#locale = 'zh_TW' """

""" url = 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:'+str(bib)+'&fromLocationLink=false&theme=mobile&showAll=true&locale='+locale
response = urllib.request.urlopen(url)
htmlbytes = response.read()
bs = BeautifulSoup(htmlbytes, "html.parser") """

#get single book-info, required before "table_book = bs.find('div', class_='itemFields').table"


#for use in other file
def get_info(bib):
    global book, copies
    def get_value(book_info_type):
        td = table_book.find('td', string=book_info_type)     #td where item name is placed
        if td != None:
            book_info = td.find_next_sibling('td').string      #next td is the value of the item
            if book_info == None:                               #sometimes the info has > 1 line. td is empty. Those info are placed in the divs inside that td
                book_info = ''
                divs = td.find_next_sibling('td').find_all('div')
                for div in divs:
                    book_info = book_info + div.string + '\n'
        else:
            return 'no info on '+ book_info_type
            """ book_info = divs[0].string + '\n ' + divs[1].string """
        return book_info

    url = 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:'+str(bib)+'&fromLocationLink=false&theme=mobile&showAll=true&locale=en'
    response = urllib.request.urlopen(url)
    htmlbytes = response.read()
    bs = BeautifulSoup(htmlbytes, "html.parser")
    #book
    book = []
    book_title = bs.find('h1', class_='title').string
    book.append(book_title)
    table_book = bs.find('div', class_='itemFields').table   #need this line before get_value()
    items = ['Author', 'Bib ID', 'Call Number', 'Physical Description', 'Place of Publication', 'Publisher',
    'Year', 'Series Title', 'Subject', 'Added Author', 'Standard No.', 'Language']
    for item in items:
        book.append(get_value(item))
    book.append(str(datetime.date.today()))
    book.append(str(datetime.date.today()))
    tuple(book)
    #copies
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

    return (book,copies)

print(get_info(3563388))
    
    



""" #get book copies
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
    i += 1 """



""" print(book_title)

for x in list:
    print(get_value(x))
print('----------------------------')
print(copies,len(copies),sep = '\n') """


#things to add
#handle case when get_value() is used b4 finding the table

#why has to put get_value() inside?

#trs = bs.find('div', class_='itemFields').find_all('tr')
#print(trs)

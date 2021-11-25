import urllib.request
from bs4 import BeautifulSoup

#testing Bib
#2835575
#3632431

#config
bib = 3563388
locale = 'en'
locale = 'zh_TW'
url = 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:'+str(bib)+'&fromLocationLink=false&theme=mobile&showAll=true&locale=zh_TW'
response = urllib.request.urlopen(url)
htmlbytes = response.read()
bs = BeautifulSoup(htmlbytes, "html.parser")


table_book_info = bs.find('div', class_='itemFields').table
def value_of(book_info_type):
    
    book_info = table_book_info.find('td', string=book_info_type).find_next_sibling('td').string
    if book_info == None:
        divs = table_book_info.find('td', string=book_info_type).find_next_sibling('td').find_all('div')
        book_info = divs[0].string + '\n ' + divs[1].string
    return book_info


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


print(
value_of('館藏編目號碼'),
value_of('索書號'),
value_of('著者'),
value_of('出版地'),
value_of('出版者'),
value_of('出版年份'),
value_of('標準號碼'),
value_of('語言'),
sep = '\n'
)
print('----------------------------')
print(copies,len(copies),sep = '\n')

#start = time.time()
#end = time.time()
#print('time spent by calling function 6 times = '+str(end-start))


#trs = bs.find('div', class_='itemFields').find_all('tr')
#print(trs)

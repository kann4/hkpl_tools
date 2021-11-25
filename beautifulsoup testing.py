import urllib.request
from bs4 import BeautifulSoup

#testing Bib
#2835575
#3632431

#config
bib = 3563388
#locale = 'en'
locale = 'zh_TW'

url = 'https://webcat.hkpl.gov.hk/lib/item?id=chamo:'+str(bib)+'&fromLocationLink=false&theme=mobile&showAll=true&locale='+locale
response = urllib.request.urlopen(url)
htmlbytes = response.read()
bs = BeautifulSoup(htmlbytes, "html.parser")

#get book info
table_book_info = bs.find('div', class_='itemFields').table
def get_value(book_info_type):
    
    book_info = table_book_info.find('td', string=book_info_type).find_next_sibling('td').string
    if book_info == None:
        divs = table_book_info.find('td', string=book_info_type).find_next_sibling('td').find_all('div')
        book_info = divs[0].string + '\n ' + divs[1].string
    return book_info

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

list = ['館藏編目號碼','索書號','著者','著錄','出版地','出版者','出版年份','主題','標準號碼','語言']
for x in list:
    print(get_value(x))
""" print(
get_value('館藏編目號碼'),
get_value('索書號'),
get_value('著者'),
get_value('著錄'),
get_value('出版地'),
get_value('出版者'),
get_value('出版年份'),
get_value('主題'),
get_value('標準號碼'),
get_value('語言'),
sep = '\n'
) """
print('----------------------------')
print(copies,len(copies),sep = '\n')

#not solved:
#more than 2 lines of info

#start = time.time()
#end = time.time()
#print('time spent by calling function 6 times = '+str(end-start))


#trs = bs.find('div', class_='itemFields').find_all('tr')
#print(trs)

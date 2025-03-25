import sys
import time
from db import insertIntoTables

if len(sys.argv) >= 2:
    for i in range(len(sys.argv)):
        if i > 0:
            bib = sys.argv[i]
            insertIntoTables(bib)
else:
    bibs = input('Enter a BIB or multiple(seperate by space):\n')
    start_time = time.time()
    bibs = bibs.split()
    for bib in bibs:
        insertIntoTables(bib)
print("--- %s seconds ---" % (time.time() - start_time))
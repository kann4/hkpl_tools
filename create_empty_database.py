import sqlite3

# Connect to database file (creates new file if it doesn't exist)
conn = sqlite3.connect('hkpl_tools.db')

# Define the SQL statements to create three tables
create_table1 = '''CREATE TABLE "Book" (
                        "bookID"	INTEGER NOT NULL UNIQUE,
                        "bookName"	TEXT,
                        "author"	TEXT,
                        "bibID"	TEXT NOT NULL UNIQUE,
                        "callNumber"	TEXT NOT NULL,
                        "physicalDescription"	TEXT,
                        "placeOfPublication"	TEXT,
                        "publisher"	TEXT,
                        "publicationYear"	TEXT,
                        "seriesTitle"	TEXT,
                        "subject"	TEXT,
                        "addedAuthor"	TEXT,
                        "standardNumber"	TEXT,
                        "language"	TEXT,
                        "creationDate"	TEXT,
                        "lastUpdateDate"	TEXT,
                        PRIMARY KEY("bookID" AUTOINCREMENT)
                    )'''

create_table2 = '''CREATE TABLE "BookCopy" (
                        "bookCopyID"	INTEGER NOT NULL UNIQUE,
                        "bookID"	INTEGER NOT NULL,
                        "libraryID"	INTEGER NOT NULL,
                        "status"	TEXT,
                        "dueDate"	TEXT,
                        "collection"	TEXT,
                        "creationDate"	TEXT,
                        "lastUpdateDate"	TEXT,
                        PRIMARY KEY("bookCopyID" AUTOINCREMENT),
                        FOREIGN KEY("libraryID") REFERENCES "Library"("libraryID"),
                        FOREIGN KEY("bookID") REFERENCES "Book"("bookID")
                    )'''

create_table3 = '''CREATE TABLE "Library" (
                        "libraryID"	INTEGER NOT NULL UNIQUE,
                        "libraryNumber"	INTEGER NOT NULL,
                        "chineseName"	TEXT,
                        "englishName"	TEXT,
                        "lastUpdateDate"	TEXT,
                        PRIMARY KEY("libraryID" AUTOINCREMENT)
                    )'''

# Execute the SQL statements to create the tables
conn.execute(create_table1)
conn.execute(create_table2)
conn.execute(create_table3)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully")
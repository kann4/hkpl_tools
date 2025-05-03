from dataclasses import dataclass
from typing import Optional


@dataclass
class LibraryModel:
    libraryID: int
    englishName: str = ''
    chineseName: str = ''
    creationDate: Optional[str] = None
    lastUpdateDate: Optional[str] = None


@dataclass
class BookModel:
    bookID: int
    bookName: Optional[str] = None
    author: Optional[str] = None
    bibID: str = ''
    callNumber: str = ''
    physicalDescription: Optional[str] = None
    placeOfPublication: Optional[str] = None
    publisher: Optional[str] = None
    publicationYear: Optional[str] = None
    seriesTitle: Optional[str] = None
    subject: Optional[str] = None
    addedAuthor: Optional[str] = None
    standardNumber: Optional[str] = None
    language: Optional[str] = None
    creationDate: Optional[str] = None
    lastUpdateDate: Optional[str] = None


@dataclass
class BookCopyModel:
    bookCopyID: int
    book: BookModel
    library: LibraryModel
    status: Optional[str] = None
    dueDate: Optional[str] = None
    collection: Optional[str] = None
    creationDate: Optional[str] = None
    lastUpdateDate: Optional[str] = None

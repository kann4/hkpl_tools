# Application Routes Documentation

## Route: `/`
### HTTP Methods:
```http
GET /
POST /
```

### GET
- Returns: Home page (index.html)

### POST
- Actions:
  - Add book by bib/url
  - Show available books
  - Update books status

## Route: `/search`
### HTTP Methods:
```http
GET /search
POST /search
```

### GET
- Returns: Search page (search.html)

### POST
- Parameters:
  - `search_term`: String
- Returns: Search results

## Route: `/Saved_Books`
### HTTP Methods:
```http
GET /Saved_Books
POST /Saved_Books
```

### GET
- Returns: Saved books page (books.html)

### POST
- Actions:
  - Delete saved books

## Route: `/user_guide`
### HTTP Methods:
```http
GET /user_guide
```

### GET
- Returns: User guide page (user_guide.html)
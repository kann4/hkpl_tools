# Todo
- bug: books in reserve libraries count as existing in those libraries for "unwanted"

- use dictionary instead of list
- soft delete
- sperate route for update/check library
- -------------
- fix: if update failed for some book, last update is misleading
- last update sometimes get from copies table, sometimes timenow
- log successful update times as default display
- fewer db connection?
  
-------------------------
- explain how server and client interact: html files, what template is actually doin, etc
- optimize some sql queries
- better loading UI eg. when updating 
  - disable button 
  - show progress
- more efficient update
  - (done) partial update based on selected library
  - concurrent http request
- better filter eg. allow per column filter, dropdown instead of textbox
- better way to do fav_libraries
- add foreign keys
- (DONE) in library lookup, allow removing books that are also available in another library
- (NO NEED) maintain single db connection?
- decouple frontend and backend?



-- from review-deepseek-r1 -- (see joplin)
- Monolithic Route Handlers
  Business logic for URL parsing, database operations, and updates are all in route handlers (lines 19-55)
  Violates Single Responsibility Principle
  Makes testing and maintenance difficult
- Code Structure
  Mixed abstraction levels (URL parsing next to DB calls)
  Helper function get_last_update_text in route file (line 13)
  Tight coupling to inserting_data_to_db module
- Potential Performance Issues
  updateCopies() may lack batch operations (line 46)
  No visible connection pooling (needs db.py review)
  Synchronous execution of updateCopies() could block
- Architectural Flaws
  Data access layer mixed with business logic
  Tight coupling to SQLite implementation
  Web scraping dependency (beautifulsoup) in data layer
- Resource Leak Risks
  Multiple code paths without proper connection cleanup
  No context managers for database resources
  Possible unclosed cursors in error scenarios
- sqlalchemy?
- Architectural Changes:
# Proposed layer separation
src/
├── web/          # Flask routes
├── services/     # Business logic
├── dal/          # Data access
└── models/       # Data models
- decouple business layer and data acess layer
  eg. web scraping directly in db.py
  eg. business rule in db.py
  eg. db call in app.py (presentation layer)


- add hkpl_scraper_base and convert book_lookup and beautifulsoup into subclass
- search form partial update
  ```
  <!-- search.html -->
  <form hx-get="/search" hx-target="#results">
    <input type="search" name="q">
  </form>
  <div id="results">
    {% include "partials/results.html" %}
  </div>
  ```
- 
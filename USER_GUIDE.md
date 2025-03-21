# HKPL Tools User Guide

## Application Workflow

```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant Database
    participant HKPLWebsite
    
    User->>WebUI: Enters BIB ID/URL
    WebUI->>HKPLWebsite: Scrapes book data
    HKPLWebsite-->>WebUI: Returns book details
    WebUI->>Database: Stores book metadata
    WebUI-->>User: Shows save confirmation
    
    User->>WebUI: Selects library
    WebUI->>Database: Queries available copies
    Database-->>WebUI: Returns availability data
    WebUI-->>User: Displays library availability
    
    User->>WebUI: Clicks "Update Copies"
    WebUI->>HKPLWebsite: Checks current status
    HKPLWebsite-->>WebUI: Returns latest data
    WebUI->>Database: Updates records
    WebUI-->>User: Shows update status
    
    User->>WebUI: Views Saved Books
    WebUI->>Database: Retrieves tracked books
    Database-->>WebUI: Returns book list
    WebUI-->>User: Displays management interface
```

## Core Features

### 1. Book Tracking
- **Supported Inputs**:
  - Direct BIB numbers (e.g. 147569)
  - HKPL website URLs
- **Data Processing**:
  - Automatic URL parsing
  - Real-time availability checks
  - Multi-library support

### 2. Availability Monitoring
- **Library Selection**:
  - Dropdown with 20+ branches
  - Last update timestamp
- **Display Format**:
  ```html
  <table>
    <tr>
      <th>Title</th><th>Call No.</th>
      <th>Status</th><th>Collection</th>
    </tr>
    <!-- Dynamic rows -->
  </table>
  ```

### 3. Data Management
- **Update System**:
  - Manual trigger via UI
  - Batch processing
  - Error reporting
- **Book Management**:
  - Bulk delete interface
  - Soft delete (planned)
  - Version history (planned)
# Bookstore Management System

A simple Python-based bookstore management system that allows you to manage book inventory using SQLite database.

## Features

- **Add Books**: Enter new books with title, author, and quantity
- **Update Books**: Modify existing book information
- **Delete Books**: Remove books from inventory with confirmation
- **Search Books**: Find books by author name
- **Database Management**: Automatic SQLite database creation and management

## Requirements

- Python 3.x
- SQLite3 (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WernerTheronKotze/gitTask2.git
   cd gitTask2
   ```

2. Run the application:
   ```bash
   python bookstore.py
   ```

## Usage

When you run the application, you'll see a menu with the following options:

```
1. Enter Book
2. Update Book
3. Delete Book
4. Search Book
0. Exit
```

### Adding a Book
- Select option 1
- Enter the book title
- Enter the author name
- Enter the quantity available

### Updating a Book
- Select option 2
- Enter the book ID you want to update
- Enter the new title, author, and quantity

### Deleting a Book
- Select option 3
- Enter the book ID to delete
- Confirm deletion when prompted

### Searching for Books
- Select option 4
- Enter the author name to search for
- All books by that author will be displayed

## Database Schema

The application uses a SQLite database (`ebookstore.db`) with the following table structure:

```sql
CREATE TABLE books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(255),
    Author VARCHAR(30),
    Qty INTEGER
)
```

## File Structure

```
gitTask2/
├── bookstore.py          # Main application file
├── ebookstore.db         # SQLite database file
├── README.md            # This file
└── SE L2T13 - Capstone Project I.pdf  # Project documentation
```

## Features in Detail

### Database Management
- Automatic database creation if it doesn't exist
- Auto-incrementing primary key for book IDs
- Data validation and error handling

### User Interface
- Simple command-line interface
- Input validation
- Confirmation prompts for destructive operations
- Clear error messages

### Data Operations
- **CREATE**: Add new books to inventory
- **READ**: Search and display books
- **UPDATE**: Modify existing book information
- **DELETE**: Remove books with confirmation

## Error Handling

The application includes basic error handling for:
- Invalid menu choices
- Non-existent book IDs
- Database connection issues
- Input validation

## Future Enhancements

Potential improvements for future versions:
- ISBN support
- Book categories/genres
- Price tracking
- Export/import functionality
- Web interface
- User authentication
- Advanced search options

## Author

**Werner Theron Kotze**
- GitHub: [WernerTheronKotze](https://github.com/WernerTheronKotze)

## License

This project is part of the Software Engineering L2T13 Capstone Project.

---

*This is a simple bookstore management system created as part of a software engineering course project.*

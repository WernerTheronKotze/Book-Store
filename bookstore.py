import sqlite3
import os
from typing import Optional, List, Tuple


class BookStore:
    """A class to manage book store operations with proper database handling."""
    
    def __init__(self, db_path: str = 'ebookstore.db'):
        """Initialize the BookStore with database connection."""
        self.db_path = db_path
        self.db = None
        self.cur = None
        self._connect_database()
        self._initialize_database()
    
    def _connect_database(self):
        """Establish database connection."""
        try:
            self.db = sqlite3.connect(self.db_path)
            self.cur = self.db.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def _initialize_database(self):
        """Create the books table if it doesn't exist."""
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS books(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(30) NOT NULL,
                    qty INTEGER NOT NULL CHECK(qty >= 0)
                )
            ''')
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise
    
    def close(self):
        """Close database connection."""
        if self.db:
            self.db.close()
    
    def enter_book(self) -> bool:
        """Add a new book to the database."""
        title = input('Enter the Book Title: ').strip()
        if not title:
            print("Error: Book title cannot be empty.")
            return False
            
        author = input('Enter the Author Name: ').strip()
        if not author:
            print("Error: Author name cannot be empty.")
            return False
        
        while True:
            try:
                qty = int(input('Enter the quantity of {} available: '.format(title)))
                if qty < 0:
                    print("Error: Quantity cannot be negative.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid integer for quantity.")
        
        try:
            self.cur.execute('INSERT INTO books(title, author, qty) VALUES (?, ?, ?)', 
                           (title, author, qty))
            self.db.commit()
            print(f"Successfully added book '{title}' by {author} with quantity {qty}")
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return False
    
    def update_book(self) -> bool:
        """Update an existing book in the database."""
        while True:
            try:
                book_id = int(input('Enter the id of book that you want to update: '))
                if book_id <= 0:
                    print("Error: ID must be a positive integer.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid integer for ID.")
        
        # Check if book exists
        try:
            self.cur.execute('SELECT id FROM books WHERE id=?', (book_id,))
            if not self.cur.fetchone():
                print(f"No book found with ID {book_id}")
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
        title = input('Enter the new title: ').strip()
        if not title:
            print("Error: Book title cannot be empty.")
            return False
        
        author = input('Enter the updated author name: ').strip()
        if not author:
            print("Error: Author name cannot be empty.")
            return False
        
        while True:
            try:
                qty = int(input('Enter the new quantity: '))
                if qty < 0:
                    print("Error: Quantity cannot be negative.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid integer for quantity.")
        
        try:
            self.cur.execute('UPDATE books SET title=?, author=?, qty=? WHERE id=?', 
                           (title, author, qty, book_id))
            self.db.commit()
            print(f"Successfully updated book with ID {book_id}")
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return False
    
    def delete_book(self) -> bool:
        """Delete a book from the database."""
        while True:
            try:
                book_id = int(input('Enter the book id to delete: '))
                if book_id <= 0:
                    print("Error: ID must be a positive integer.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid integer for ID.")
        
        try:
            self.cur.execute('SELECT title FROM books WHERE id=?', (book_id,))
            result = self.cur.fetchone()
            
            if result:
                print(f"Found book: {result[0]}")
                choice = input('Are you sure, you want to delete the book with id {} (y/n): '.format(book_id))
                if choice.lower() in ['y', 'yes']:
                    self.cur.execute('DELETE FROM books WHERE id=?', (book_id,))
                    self.db.commit()
                    print(f"Successfully deleted book with ID {book_id}")
                    return True
                else:
                    print("Deletion cancelled.")
                    return False
            else:
                print('No book with the given id found')
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return False
    
    def search_book(self) -> bool:
        """Search for books by author name."""
        author = input('Input the author name to search book for: ').strip()
        if not author:
            print("Error: Author name cannot be empty.")
            return False
        
        try:
            # Use wildcards for partial matching
            search_pattern = f'%{author}%'
            self.cur.execute('SELECT * FROM books WHERE author LIKE ?', (search_pattern,))
            results = self.cur.fetchall()
            
            if results:
                print("\nSearch Results:")
                print("ID | Title | Author | Quantity")
                print("-" * 40)
                for row in results:
                    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                print(f"\nFound {len(results)} book(s)")
                return True
            else:
                print('No books found')
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("           eBookStore Management System")
    print("="*50)
    print("1. Enter Book")
    print("2. Update Book")
    print("3. Delete Book")
    print("4. Search Book")
    print("0. Exit")
    print("="*50)


def main():
    """Main function to run the book store application."""
    # Initialize the book store
    bookstore = BookStore()
    
    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                bookstore.enter_book()
            elif choice == '2':
                bookstore.update_book()
            elif choice == '3':
                bookstore.delete_book()
            elif choice == '4':
                bookstore.search_book()
            elif choice == '0':
                print('\nThank you for visiting eBookStore!!')
                break
            else:
                print('Invalid choice. Please try again...')
    
    except KeyboardInterrupt:
        print('\n\nApplication interrupted by user.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        bookstore.close()


if __name__ == '__main__':
    main()
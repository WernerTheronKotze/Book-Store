import sqlite3    # Utility module for working with Database


def validate_quantity(qty_str):
    """Validate and convert quantity input to integer."""
    try:
        qty = int(qty_str)
        if qty < 0:
            raise ValueError("Quantity cannot be negative")
        return qty
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid positive integer.")
        return None


def validate_id(id_str):
    """Validate and convert ID input to integer."""
    try:
        book_id = int(id_str)
        if book_id <= 0:
            raise ValueError("ID must be a positive integer")
        return book_id
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid positive integer.")
        return None


def enter_book():
    title = input('Enter the Book Title: ').strip()
    if not title:
        print("Error: Book title cannot be empty.")
        return
    
    author = input('Enter the Author Name: ').strip()
    if not author:
        print("Error: Author name cannot be empty.")
        return
    
    while True:
        qty_str = input('Enter the quantity of {} available: '.format(title))
        qty = validate_quantity(qty_str)
        if qty is not None:
            break

    try:
        cur.execute('INSERT INTO books(title, author, qty) values (?, ?, ?)', (title, author, qty))
        db.commit()
        print(f"Successfully added book '{title}' by {author} with quantity {qty}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        db.rollback()


def update_book():
    while True:
        id_str = input('Enter the id of book that you want to update: ')
        book_id = validate_id(id_str)
        if book_id is not None:
            break
    
    # Check if book exists
    try:
        cur.execute('SELECT id FROM books WHERE id=?', (book_id,))
        if not cur.fetchone():
            print(f"No book found with ID {book_id}")
            return
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return
    
    title = input('Enter the new title: ').strip()
    if not title:
        print("Error: Book title cannot be empty.")
        return
    
    author = input('Enter the updated author name: ').strip()
    if not author:
        print("Error: Author name cannot be empty.")
        return
    
    while True:
        qty_str = input('Enter the new quantity: ')
        qty = validate_quantity(qty_str)
        if qty is not None:
            break

    try:
        cur.execute('UPDATE books SET title=?, author=?, qty=? WHERE id=?', (title, author, qty, book_id))
        db.commit()
        print(f"Successfully updated book with ID {book_id}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        db.rollback()


def delete_book():
    while True:
        id_str = input('Enter the book id to delete: ')
        book_id = validate_id(id_str)
        if book_id is not None:
            break
    
    try:
        cur.execute('SELECT title from books WHERE id=?', (book_id,))
        results = cur.fetchone()
        
        if results:
            print(f"Found book: {results[0]}")
            choice = input('Are you sure, you want to delete the book with id {} (y/n): '.format(book_id))
            if choice.lower() in ['y', 'yes']:
                cur.execute('DELETE FROM books WHERE id=?', (book_id,))
                db.commit()
                print(f"Successfully deleted book with ID {book_id}")
            else:
                print("Deletion cancelled.")
        else:
            print('No book with the given id found')
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        db.rollback()


def search_book():
    author = input('Input the author name to search book for: ').strip()
    if not author:
        print("Error: Author name cannot be empty.")
        return

    try:
        # Use wildcards for partial matching
        search_pattern = f'%{author}%'
        cur.execute('SELECT * FROM books WHERE author LIKE ?', (search_pattern,))
        results = cur.fetchall()
        
        if results:
            print("\nSearch Results:")
            print("ID | Title | Author | Quantity")
            print("-" * 40)
            for row in results:
                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
            print(f"\nFound {len(results)} book(s)")
        else:
            print('No books found')
    except sqlite3.Error as e:
        print(f"Database error: {e}")


if __name__ == '__main__':
    db = sqlite3.connect('ebookstore.db')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS books('
               'id integer primary key AUTOINCREMENT,'
                'Title varchar(255),'
               'Author varchar(30),'
               'Qty integer)')

    while True:
        choice = input('1. Enter Book\n'
                       '2. Update Book\n'
                       '3. Delete Book\n'
                       '4. Search Book\n'
                       '0. Exit: ')
        if choice == '1':
            enter_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_book()
        elif choice == '0':
            break
        else:
            print('Wrong Choice, Try again...')

    print('Thank you for visiting eBookStore!!')
    db.close()
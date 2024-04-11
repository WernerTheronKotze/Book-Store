import sqlite3    # Utility module for working with Database


def enter_book():
    title = input('Enter the Book Title: ')
    author = input('Enter the Author Name: ')
    qty = input('Enter the quantity of {} available: '.format(title))

    cur.execute('INSERT INTO books(title, author, qty) values (?, ?, ?)', (title, author, qty))  # Insert the values
    db.commit()    # Save the changes


def update_book():
    id = input('Enter the id of book that you want to update: ')
    title = input('Enter the new title: ')
    author = input('Enter the updated author name: ')
    qty = input('Enter the new quantity: ')

    cur.execute('UPDATE books SET title=?, author=?, qty=? WHERE id=?', (title, author, qty, id))    # Set the new values
    db.commit()


def delete_book():
    id = input('Enter the book id to delete: ')
    cur.execute('SELECT title from books WHERE id=?', (id,))
    results = cur.fetchone()    # Fetch only one entry from above executed statement
    print(results)
    if results:
        choice = input('Are you sure, you want to delete the book with id {}(1/0): '.format(results[0]))
    else:
        print('No book with the given id found')
        return
    if choice == '1':
        cur.execute('DELETE FROM books WHERE id=?', (id,))
    db.commit()


def search_book():
    author = input('Input the author name to search book for: ')

    cur.execute('SELECT * FROM books where author like ?', (author,))
    results = cur.fetchall()    # Fetch all results from above statement
    if results:
        for row in results:
            print(str(row[0]) + ' | ' + row[1] + ' | ' + row[2] + ' | ' + str(row[3]))
    else:
        print('No books found')


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
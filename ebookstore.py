import sqlite3

def connect_to_db():
    """
    Connects to the ebookstore database.
    
    Returns:
        sqlite3.Connection: A connection to the ebookstore database.
    """
    return sqlite3.connect('ebookstore.db')

def create_table():
    """
    Creates a new table for books if it doesn't already exist.
    The table has columns: id, title, author, and quantity.
    """
    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS book
                        (id INTEGER PRIMARY KEY, 
                        title TEXT NOT NULL, 
                        author TEXT NOT NULL, 
                        qty INTEGER NOT NULL)''')
        connection.commit()

def add_books(books):
    """
    Adds a list of books to the database.
    
    Args:
        books (list): List of books to add.
    """
    with connect_to_db() as connection:
        cursor = connection.cursor()
        for book in books:
            cursor.execute("INSERT OR IGNORE INTO book(id, title, author, qty) VALUES (?, ?, ?, ?)", book)
        connection.commit()

def enter_book():
    """
    Prompts user for book details and adds the book to the database.
    """
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    qty = int(input("Enter the quantity of the book: "))

    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO book(title, author, qty) VALUES (?, ?, ?)", (title, author, qty))
        connection.commit()
        print(f"Book {title} added successfully!")

def update_book():
    """
    Prompts user for a books ID and then updates the book details in the database.
    """
    book_id = input("Enter the ID of the book to update: ")

    title = input("Enter the new title of the book (or press enter to skip): ")
    author = input("Enter the new author of the book (or press enter to skip): ")
    qty = input("Enter the new quantity of the book (or press enter to skip): ")

    with connect_to_db() as connection:
        cursor = connection.cursor()

        if title:
            cursor.execute("UPDATE book SET title = ? WHERE id = ?", (title, book_id))
        if author:
            cursor.execute("UPDATE book SET author = ? WHERE id = ?", (author, book_id))
        if qty:
            cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (qty, book_id))

        connection.commit()
        print(f"Book with ID {book_id} updated successfully!")

def delete_book():
    """
    Prompts user for a book's ID and then deletes the book from the database.
    """
    book_id = input("Enter the ID of the book to delete: ")

    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
        connection.commit()
        print(f"Book with ID {book_id} deleted successfully!")

def search_book():
    """
    Prompts user for a search query and then searches the database for matching books by title, author, or ID.
    """
    query = input("Enter your search query (title, author, or ID): ")

    with connect_to_db() as connection:
        cursor = connection.cursor()
        if query.isdigit():
            cursor.execute("SELECT * FROM book WHERE id=?", (query,))
        else:
            cursor.execute("SELECT * FROM book WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()
        if results:
            for book in results:
                print(book)
        else:
            print("No books found with that query.")

def main():
    create_table()

    books_to_add = [
        (3001, 'A Tale Of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter And The Philosophers Stone', 'J.K Rowling', 40),
        (3003, 'The Lion, The Witch And The Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    add_books(books_to_add)

    while True:
        print("\nMENU:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search book")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            enter_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_book()
        elif choice == "0":
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()

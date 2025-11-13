from library.models import Book, Borrower
from library.library import Library
from library.utils import format_date
import sys

lib = Library()

def seed_sample_data():
    lib.add_book(Book("The Pragmatic Programmer", "Andrew Hunt", "9780201616224", "Programming", 3))
    lib.add_book(Book("Clean Code", "Robert Martin", "9780132350884", "Programming", 2))
    lib.add_borrower(Borrower("Alice", "alice@mail.com", "MEM001"))
    lib.add_borrower(Borrower("Bob", "bob@mail.com", "MEM002"))

def print_menu():
    print("\n===== Library Menu =====")
    print("1. Add book")
    print("2. Update book")
    print("3. Remove book")
    print("4. List books")
    print("5. Add borrower")
    print("6. Update borrower")
    print("7. Remove borrower")
    print("8. List borrowers")
    print("9. Borrow book")
    print("10. Return book")
    print("11. Borrower loans")
    print("12. Search books")
    print("0. Exit")

def input_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        return None

# COMMANDS ----------------------------------------------------------

def cmd_add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()
    genre = input("Genre: ").strip()
    qty = input_int("Quantity: ")
    if qty is None:
        print("Invalid quantity.")
        return

    book = Book(title, author, isbn, genre, qty)
    book_id = lib.add_book(book)
    print(f"Book added with id {book_id}")

def cmd_update_book():
    book_id = input_int("Book ID: ")
    book = lib.get_book(book_id)

    if not book:
        print("Book not found.")
        return

    print("Leave field blank to keep original value.")
    title = input(f"Title ({book.title}): ").strip() or book.title
    author = input(f"Author ({book.author}): ").strip() or book.author
    isbn = input(f"ISBN ({book.isbn}): ").strip() or book.isbn
    genre = input(f"Genre ({book.genre}): ").strip() or book.genre
    qty = input(f"Quantity ({book.quantity}): ").strip()

    try:
        qty = int(qty) if qty else book.quantity
    except:
        print("Invalid quantity.")
        return

    lib.update_book(book_id, title=title, author=author, isbn=isbn, genre=genre, quantity=qty)
    print("Book updated successfully.")

def cmd_remove_book():
    book_id = input_int("Book ID: ")
    if lib.remove_book(book_id):
        print("Book removed.")
    else:
        print("Cannot remove book (still borrowed or not found).")

def cmd_list_books():
    books = lib.list_books()
    if not books:
        print("No books found.")
        return

    print("\nID | Title | Author | ISBN | Genre | Qty")
    for b in books:
        print(f"{b.id} | {b.title} | {b.author} | {b.isbn} | {b.genre} | {b.quantity}")

def cmd_add_borrower():
    name = input("Name: ")
    contact = input("Contact: ")
    membership = input("Membership ID: ")

    b = Borrower(name, contact, membership)
    bid = lib.add_borrower(b)
    print(f"Borrower added with id {bid}")

def cmd_update_borrower():
    borrower_id = input_int("Borrower ID: ")
    b = lib.get_borrower(borrower_id)

    if not b:
        print("Borrower not found.")
        return

    name = input(f"Name ({b.name}): ").strip() or b.name
    contact = input(f"Contact ({b.contact}): ").strip() or b.contact
    mem = input(f"Membership ID ({b.membership_id}): ").strip() or b.membership_id

    lib.update_borrower(borrower_id, name=name, contact=contact, membership_id=mem)
    print("Borrower updated.")

def cmd_remove_borrower():
    borrower_id = input_int("Borrower ID: ")
    if lib.remove_borrower(borrower_id):
        print("Borrower removed.")
    else:
        print("Cannot remove borrower (still borrowing).")

def cmd_list_borrowers():
    borrowers = lib.list_borrowers()

    print("\nID | Name | Contact | Membership")
    for b in borrowers:
        print(f"{b.id} | {b.name} | {b.contact} | {b.membership_id}")

def cmd_borrow_book():
    borrower_id = input_int("Borrower ID: ")
    book_id = input_int("Book ID: ")

    due = lib.borrow_book(borrower_id, book_id)
    if due:
        print(f"Book borrowed. Due date: {format_date(due)}")
    else:
        print("Borrow failed.")

def cmd_return_book():
    borrower_id = input_int("Borrower ID: ")
    book_id = input_int("Book ID: ")

    if lib.return_book(borrower_id, book_id):
        print("Book returned.")
    else:
        print("Return failed.")

def cmd_borrower_loans():
    borrower_id = input_int("Borrower ID: ")
    loans = lib.borrowed_books_for_borrower(borrower_id)

    if not loans:
        print("No borrowed books.")
        return

    print("\nBorrowed Books:")
    for loan in loans:
        book = loan["book"]
        print(f"{book.title} | {format_date(loan['due_date'])}")

def cmd_search_books():
    print("Search by: 1-title 2-author 3-genre 4-isbn")
    c = input_int("Choice: ")

    field_map = {1: "title", 2: "author", 3: "genre", 4: "isbn"}
    field = field_map.get(c, "title")

    query = input("Enter search text: ")
    results = lib.search(query, field)

    if not results:
        print("No books found.")
        return

    print("\nID | Title | Author | Qty")
    for b in results:
        print(f"{b.id} | {b.title} | {b.author} | {b.quantity}")

# MAIN LOOP ----------------------------------------------------------

def main():
    seed_sample_data()
    while True:
        print_menu()
        choice = input_int("Choose: ")

        if choice == 0:
            print("Goodbye!")
            sys.exit()

        commands = {
            1: cmd_add_book,
            2: cmd_update_book,
            3: cmd_remove_book,
            4: cmd_list_books,
            5: cmd_add_borrower,
            6: cmd_update_borrower,
            7: cmd_remove_borrower,
            8: cmd_list_borrowers,
            9: cmd_borrow_book,
            10: cmd_return_book,
            11: cmd_borrower_loans,
            12: cmd_search_books,
        }

        func = commands.get(choice)
        if func:
            func()
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()

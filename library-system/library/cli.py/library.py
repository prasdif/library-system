from typing import Dict, List, Optional
from datetime import date, timedelta
from .models import Book, Borrower
import itertools

class Library:
    def __init__(self, loan_days: int = 14):
        self._books: Dict[int, Book] = {}
        self._borrowers: Dict[int, Borrower] = {}
        self._borrowed: Dict[int, List[Dict]] = {}
        self._book_id_counter = itertools.count(1)
        self._borrower_id_counter = itertools.count(1)
        self.loan_days = loan_days

    # BOOK MANAGEMENT -----------------------------------------------------

    def add_book(self, book: Book) -> int:
        book_id = next(self._book_id_counter)
        book.id = book_id
        self._books[book_id] = book
        return book_id

    def update_book(self, book_id: int, **kwargs) -> bool:
        book = self._books.get(book_id)
        if not book:
            return False
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        return True

    def remove_book(self, book_id: int) -> bool:
        if book_id not in self._books:
            return False

        if self._borrowed.get(book_id):
            if len(self._borrowed[book_id]) > 0:
                return False

        del self._books[book_id]
        self._borrowed.pop(book_id, None)
        return True

    def list_books(self) -> List[Book]:
        return list(self._books.values())

    # BORROWER MANAGEMENT -------------------------------------------------

    def add_borrower(self, borrower: Borrower) -> int:
        borrower_id = next(self._borrower_id_counter)
        borrower.id = borrower_id
        self._borrowers[borrower_id] = borrower
        return borrower_id

    def update_borrower(self, borrower_id: int, **kwargs) -> bool:
        borrower = self._borrowers.get(borrower_id)
        if not borrower:
            return False
        for key, value in kwargs.items():
            if hasattr(borrower, key):
                setattr(borrower, key, value)
        return True

    def remove_borrower(self, borrower_id: int) -> bool:
        for book_id, loans in self._borrowed.items():
            for loan in loans:
                if loan["borrower_id"] == borrower_id:
                    return False
        return self._borrowers.pop(borrower_id, None) is not None

    def list_borrowers(self) -> List[Borrower]:
        return list(self._borrowers.values())

    # BORROWING / RETURNING -----------------------------------------------

    def borrow_book(self, borrower_id: int, book_id: int) -> Optional[date]:
        borrower = self._borrowers.get(borrower_id)
        book = self._books.get(book_id)

        if borrower is None or book is None:
            return None

        if book.quantity <= 0:
            return None

        book.quantity -= 1
        due_date = date.today() + timedelta(days=self.loan_days)

        self._borrowed.setdefault(book_id, []).append({
            "borrower_id": borrower_id,
            "due_date": due_date
        })

        return due_date

    def return_book(self, borrower_id: int, book_id: int) -> bool:
        loans = self._borrowed.get(book_id, [])

        for i, loan in enumerate(loans):
            if loan['borrower_id'] == borrower_id:
                loans.pop(i)
                self._books[book_id].quantity += 1

                if not loans:
                    self._borrowed.pop(book_id, None)

                return True

        return False

    def borrowed_books_for_borrower(self, borrower_id: int) -> List[Dict]:
        results = []

        for book_id, loans in self._borrowed.items():
            for loan in loans:
                if loan["borrower_id"] == borrower_id:
                    book = self._books.get(book_id)
                    results.append({
                        "book": book,
                        "due_date": loan["due_date"]
                    })

        return results

    # SEARCH & AVAILABILITY -----------------------------------------------

    def search(self, query: str, field: str = "title") -> List[Book]:
        q = query.lower().strip()
        results = []

        for book in self._books.values():
            value = getattr(book, field, "").lower()
            if q in value:
                results.append(book)

        return results

    de

from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    genre: str
    quantity: int = 1
    id: Optional[int] = None

    def is_available(self) -> bool:
        return self.quantity > 0


@dataclass
class Borrower:
    name: str
    contact: str
    membership_id: str
    id: Optional[int] = None

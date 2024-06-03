from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    year_published: int
    isbn: str
    language: str
    amount_total: int


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    amount_currently_borrowed: int
    borrow_history: str
    is_available: bool

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name_last: str
    name_first: str
    date_birth: date
    date_death: date | None
    country_of_birth: str


class AuthorUpdate(AuthorBase):
    pass


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True


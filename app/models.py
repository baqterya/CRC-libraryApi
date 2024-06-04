from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, Date, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

Base = declarative_base()


class AuthorModel(Base):
    __tablename__ = 'authors'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name_last = mapped_column(String)
    name_first = mapped_column(String)
    date_birth = mapped_column(Date)
    date_death = mapped_column(Date, nullable=True)
    country_of_birth = mapped_column(String)

    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    books = relationship('BookModel', back_populates='author')


class BookModel(Base):
    __tablename__ = 'books'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title = mapped_column(String)
    year_published = mapped_column(Integer)
    isbn = mapped_column(String)
    language = mapped_column(String)
    amount_total = mapped_column(Integer)
    amount_currently_borrowed = mapped_column(Integer)
    borrow_history = mapped_column(String)
    is_available = mapped_column(Boolean)

    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    author_id = mapped_column(Integer, ForeignKey('authors.id'))
    author = relationship('AuthorModel', back_populates='books')

    def last_borrowed(self) -> str:
        return self.borrow_history.split(',')[-1]

    def borrowed_ever(self) -> int:
        return len(self.borrow_history.split(','))

    def borrow(self):
        self.amount_currently_borrowed += 1
        if self.amount_currently_borrowed == self.amount_total:
            self.is_available = False
        self.borrow_history += f",{datetime.now()}"

    def return_(self):
        self.amount_currently_borrowed -= 1
        if not self.is_available and self.amount_currently_borrowed < self.amount_total:
            self.is_available = True

    def add_copy(self):
        self.amount_total += 1
        if self.amount_currently_borrowed < self.amount_total:
            self.is_available = True

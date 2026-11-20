-- The library's schema, with every constraint the design asks for.
CREATE TABLE person (
  person_id  INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name  TEXT NOT NULL
);
CREATE TABLE member (                      -- a person is a member at most once: 1--1
  member_id INTEGER PRIMARY KEY,
  person_id INTEGER NOT NULL UNIQUE REFERENCES person(person_id),
  joined    TEXT NOT NULL
);
CREATE TABLE book (
  book_id INTEGER PRIMARY KEY,
  title   TEXT NOT NULL,
  author  TEXT NOT NULL,
  pages   INTEGER CHECK (pages > 0)
);
CREATE TABLE loan (                        -- the association table of borrows: *--*
  loan_id     INTEGER PRIMARY KEY,
  book_id     INTEGER NOT NULL REFERENCES book(book_id),
  member_id   INTEGER NOT NULL REFERENCES member(member_id),
  out_date    TEXT NOT NULL,
  due_date    TEXT NOT NULL,
  return_date TEXT,                        -- NULL while the book is out
  CHECK (due_date > out_date),
  CHECK (return_date IS NULL OR return_date >= out_date)
);

-- A small library, with its keys and constraints.
CREATE TABLE street (
  street_id INTEGER PRIMARY KEY,
  name      TEXT NOT NULL,
  postcode  TEXT NOT NULL CHECK (postcode LIKE 'B-___')
);
CREATE TABLE member (
  member_id INTEGER PRIMARY KEY,
  name      TEXT NOT NULL,
  street_id INTEGER NOT NULL REFERENCES street(street_id)
);
CREATE TABLE book (
  book_id INTEGER PRIMARY KEY,
  title   TEXT NOT NULL,
  author  TEXT NOT NULL,
  year    INTEGER CHECK (year BETWEEN 1450 AND 2100)
);
CREATE TABLE loan (
  loan_id     INTEGER PRIMARY KEY,
  book_id     INTEGER NOT NULL REFERENCES book(book_id),
  member_id   INTEGER NOT NULL REFERENCES member(member_id),
  out_date    TEXT NOT NULL,
  return_date TEXT
);

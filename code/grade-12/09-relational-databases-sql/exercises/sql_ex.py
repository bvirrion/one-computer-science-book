"""Exercises of the chapter on relational databases, run on the town's tables."""
import sqlite3

import town


def town_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    town.to_sqlite(conn)
    return conn


def count_authors(conn):                                       # exercise 3
    return conn.execute("SELECT COUNT(DISTINCT author) FROM books").fetchone()[0]


def by_author(conn, author):                                   # exercise 4
    return conn.execute("SELECT title, year FROM books WHERE author = ? ORDER BY year",
                        (author,)).fetchall()


def cross_size(conn):                                          # exercise 5
    return conn.execute("SELECT COUNT(*) FROM loans, books").fetchone()[0]


def members_still_out(conn):                                   # exercise 6
    return conn.execute(
        """SELECT DISTINCT p.first_name, p.last_name
           FROM loans AS l JOIN members AS m ON l.member_id = m.member_id
             JOIN people AS p ON m.person_id = p.person_id
           WHERE l.return_date IS NULL ORDER BY p.last_name, p.first_name""").fetchall()


def join_rows(conn):                                           # exercise 7
    q = "SELECT COUNT(*) FROM loans JOIN books ON loans.book_id = books.book_id"
    return conn.execute(q).fetchone()[0]


def extend_still_out(conn, days):                              # exercise 9
    cur = conn.execute("UPDATE loans SET due_date = date(due_date, ?) "
                       "WHERE return_date IS NULL", (f"+{days} days",))
    return cur.rowcount


def try_delete(conn, statement):                               # exercise 10
    try:
        return conn.execute(statement).rowcount
    except sqlite3.IntegrityError as error:
        return str(error)


TIMETABLE = """
CREATE TABLE teacher (teacher_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE room (room TEXT PRIMARY KEY, seats INTEGER CHECK (seats > 0));
CREATE TABLE lesson (
  day     TEXT CHECK (day IN ('Mon', 'Tue', 'Wed', 'Thu', 'Fri')),
  hour    INTEGER CHECK (hour BETWEEN 8 AND 17),
  room    TEXT REFERENCES room(room),
  teacher INTEGER REFERENCES teacher(teacher_id),
  subject TEXT NOT NULL,
  PRIMARY KEY (day, hour, room),
  UNIQUE (day, hour, teacher)
);
"""                                                            # exercise 12


def books_between(conn, first, last):                          # exercise 13
    return [row[0] for row in conn.execute(
        "SELECT title FROM books WHERE year BETWEEN ? AND ? ORDER BY year, title",
        (first, last))]

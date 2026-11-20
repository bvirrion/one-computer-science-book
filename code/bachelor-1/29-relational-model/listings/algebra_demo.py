"""algebra_demo.py: three questions about the town's library asked in relational
algebra and in SQL; the answers are compared as sets."""

import sqlite3

import town
from algebra import difference, division, natural_join, project, select, table


def sql(query):
    conn = sqlite3.connect(":memory:")
    town.to_sqlite(conn)
    return {tuple(r) for r in conn.execute(query)}


books, loans, members = table("books"), table("loans"), table("members")

# 1. Titles and years of the poetry written before 2000.
old_poetry = project(select(books, lambda t: t["genre"] == "poetry"
                            and t["year"] < 2000), ("title", "year"))
# 2. Members who never borrowed poetry: all members minus those who did.
poetry_readers = project(select(natural_join(loans, books),
                                lambda t: t["genre"] == "poetry"), ("member_id",))
never = difference(project(members, ("member_id",)), poetry_readers)
# 3. Members who borrowed every book by Kofi Elmwick: a division.
by_elmwick = project(select(books, lambda t: t["author"] == "Kofi Elmwick"),
                     ("book_id",))
every = division(project(loans, ("member_id", "book_id")), by_elmwick)

answers = [
    ("old poetry", old_poetry, "SELECT title, year FROM books "
     "WHERE genre = 'poetry' AND year < 2000"),
    ("never poetry", never, "SELECT member_id FROM members EXCEPT SELECT member_id "
     "FROM loans JOIN books USING (book_id) WHERE genre = 'poetry'"),
    ("all of Elmwick", every, "SELECT member_id FROM members AS m WHERE NOT EXISTS "
     "(SELECT * FROM books AS b WHERE b.author = 'Kofi Elmwick' AND NOT EXISTS "
     "(SELECT * FROM loans AS l WHERE l.member_id = m.member_id "
     "AND l.book_id = b.book_id))"),
]
for name, relation, query in answers:
    same = set(relation.rows) == sql(query)
    print(f"{name:14} {len(relation):2} tuple(s), the same as SQL: {same}")
print("members who borrowed all", len(by_elmwick), "books by Kofi Elmwick:",
      sorted(t[0] for t in every.rows))

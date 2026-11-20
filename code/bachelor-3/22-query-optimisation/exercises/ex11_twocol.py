"""ex11_twocol.py -- the independence assumption on two correlated columns of the
loans, and a two-column statistic that fixes it: a histogram of (month out, month
due) pairs, whose cells are counted together."""

import town

loans = town.load("loans")
n = len(loans)


def month(date):
    return int(date[5:7])


def independent(m_out, m_due):
    """Rows out before month m_out and due before m_due, if the columns were
    independent."""
    s1 = sum(month(t["out_date"]) < m_out for t in loans) / n
    s2 = sum(month(t["due_date"]) < m_due for t in loans) / n
    return n * s1 * s2


GRID = {}  # the two-column statistic: rows per (out month, due month)
for t in loans:
    cell = (month(t["out_date"]), month(t["due_date"]))
    GRID[cell] = GRID.get(cell, 0) + 1


def two_column(m_out, m_due):
    return sum(c for (mo, md), c in GRID.items() if mo < m_out and md < m_due)


if __name__ == "__main__":
    print("out before  due before  true  independent  two-column")
    for m_out, m_due in ((3, 3), (6, 6), (6, 4), (10, 12)):
        true = sum(
            month(t["out_date"]) < m_out and month(t["due_date"]) < m_due for t in loans
        )
        print(
            f"{m_out:>10}  {m_due:>10}  {true:>4}  {independent(m_out, m_due):>11.1f}"
            f"  {two_column(m_out, m_due):>10}"
        )
    print(f"the statistic has {len(GRID)} cells")

"""The exercises, the demos' numbers and the weekend problem's numbers."""

import random
import sys
from datetime import date
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises"), str(HERE / "tests")]

import ex9_steps  # noqa: E402
import ex10_metamorphic as meta  # noqa: E402
import mutate  # noqa: E402
import refactor_after  # noqa: E402
import refactor_before  # noqa: E402
import towndate  # noqa: E402
from ex6_memory_repo import MemoryLoans  # noqa: E402
from ex12_counts import LineCounts  # noqa: E402
from coverage_tool import Coverage  # noqa: E402
from loans.model import Book, Loan, Reader  # noqa: E402
from loans.repo import SqliteLoans  # noqa: E402

LISTINGS = HERE / "listings"


def test_towndate_against_datetime():
    rng = random.Random(30)
    for _ in range(2000):
        a = date.fromordinal(rng.randrange(1, 3_652_059))
        b = date.fromordinal(rng.randrange(1, 3_652_059))
        assert towndate.day_number(a.year, a.month, a.day) == a.toordinal()
        assert towndate.days_between(a.timetuple()[:3], b.timetuple()[:3]) == abs(
            (b - a).days
        )
        assert towndate.weekday(a.timetuple()[:3]) == a.strftime("%A")
        assert towndate.is_leap(a.year) == (
            (date(a.year, 3, 1) - date(a.year, 2, 1)).days > 28
        )


def test_problem_numbers():
    first = mutate.suite_of("date_tests", lambda n: not n.startswith("test_new_"))
    sys.modules.pop("towndate", None)
    with Coverage(LISTINGS / "towndate.py") as cov:
        assert first()
    assert cov.report()["statements"] == (16, 16)
    assert cov.report()["branches"] == (15, 18)
    import towndate  # noqa: F401,F811

    path = LISTINGS / "towndate.py"
    r1 = mutate.analyse("towndate", path, first)
    r2 = mutate.analyse("towndate", path, mutate.suite_of("date_tests"))
    assert (sum(r[3] for r in r1), sum(r[3] for r in r2), len(r1)) == (46, 60, 62)
    survivors = {(r[0], r[1], r[2]) for r in r2 if not r[3]}
    assert survivors == {(42, "n >= 0", "n > 0"), (42, "0", "1")}
    # the two survivors are equivalent: for every integer n the three expressions agree
    for n in range(-1000, 1001):
        assert (n if n >= 0 else -n) == (n if n > 0 else -n) == (n if n >= 1 else -n)


def test_ex5_mutation_finds_the_useless_test():
    import loans.service  # noqa: F401

    path = LISTINGS / "loans" / "service.py"
    always = mutate.suite_of("ex5_wrong_object", lambda n: n.endswith("always_passes"))
    fixed = mutate.suite_of("ex5_wrong_object", lambda n: n.endswith("fixed"))
    k1 = sum(r[3] for r in mutate.analyse("loans.service", path, always))
    k2 = sum(r[3] for r in mutate.analyse("loans.service", path, fixed))
    assert (k1, k2) == (3, 5)  # the two mutants of flat_fine survive the first test


def contract(repo):
    ada, grace = Reader("C1", "Ada"), Reader("C2", "Grace")
    day = date(2026, 3, 2)
    loan = Loan(Book("1", "Dune"), ada, day, date(2026, 3, 23))
    repo.add(loan)
    repo.add(Loan(Book("2", "Emma"), grace, day, date(2026, 3, 23)))
    loan.due = date(
        2027, 1, 1
    )  # changing the caller's object must not change the store
    assert repo.open_loan_of("1").due == date(2026, 3, 23)
    assert [x.book.isbn for x in repo.open_loans_of("C1")] == ["1"]
    back = repo.open_loan_of("1")
    back.returned = date(2026, 3, 10)
    repo.save(back)
    assert repo.open_loan_of("1") is None and repo.open_loans_of("C1") == []
    assert repo.open_loan_of("2").reader == grace


def test_ex6_contract_for_both_repositories():
    contract(SqliteLoans())
    contract(MemoryLoans())


LOANS = [
    ("Dune", "Ada", date(2026, 3, 2)),
    ("Emma", "Grace", date(2026, 2, 9)),
    ("Ulysses", "Alan", date(2026, 3, 20)),
    ("Middlemarch", "Ada", date(2026, 1, 5)),
]


@settings(max_examples=200, deadline=None)
@given(
    st.integers(0, 100),
    st.one_of(st.none(), st.integers(0, 1000)),
    st.integers(0, 30),
    st.integers(0, 120),
)
def test_ex9_every_step_prints_the_same_report(rate, cap, grace, offset):
    today = date(2026, 1, 5).fromordinal(date(2026, 1, 5).toordinal() + offset)
    args = (LOANS, today, rate, cap, grace, "EUR")
    old = refactor_before.fines_report(*args)
    assert ex9_steps.report_step1(*args) == old
    assert ex9_steps.report_step2(*args) == old
    policy = refactor_after.FinePolicy(rate, cap, grace, "EUR")
    assert refactor_after.fines_report(LOANS, today, policy) == old


def test_ex10_metamorphic_relations():
    rng = random.Random(10)
    broken = {1: 0, 2: 0, 3: 0}
    for _ in range(500):
        xs = [rng.randrange(10) for _ in range(rng.randrange(1, 9))]
        perm = list(range(len(xs)))
        rng.shuffle(perm)
        broken[1] += not meta.permuted_input_same_output(meta.merge_sort, xs, perm)
        broken[2] += not meta.doubled_input_doubled_output(meta.merge_sort, xs)
        broken[3] += not meta.shifted_input_shifted_output(meta.merge_sort, xs, 7)
        assert meta.permuted_input_same_output(sorted, xs, perm)
        assert meta.doubled_input_doubled_output(sorted, xs)
        assert meta.shifted_input_shifted_output(sorted, xs, 7)
    assert broken == {1: 0, 2: 500, 3: 0}  # only the doubling relation sees the bug


def test_ex12_line_counts():
    sys.modules.pop("towndate", None)
    with LineCounts(LISTINGS / "towndate.py") as counter:
        import towndate as fresh

        counter.counts.clear()
        fresh.day_number(2026, 3, 1)
    # y = ...; n = ...; the for line 3 times (2 turns and the exit); body twice; return
    assert sorted(counter.counts.items()) == [
        (17, 1),
        (21, 2),
        (23, 2),
        (32, 1),
        (33, 1),
        (34, 3),
        (35, 2),
        (36, 1),
    ]


def test_mutant_counts():  # exercise 8: one mutant per operator, one per integer constant
    tree = mutate.ast.parse("a + b * c < d - 1")
    assert len(mutate.sites(tree)) == 5


def test_ex4_capped_fine_mutants():
    import loans.service as service

    path = LISTINGS / "loans" / "service.py"
    seen = {}
    for line, _before, after, tree in mutate.mutants(path.read_text()):
        if line == 14:
            namespace = {}
            exec(compile(tree, str(path), "exec"), namespace)
            seen[after] = namespace["capped_fine"](30) != 500
    assert seen == {
        "20 + days_late": True,
        "21": False,
        "501": True,
    }
    assert service.capped_fine(30) == 500


def coverage_of(tmp_path, source, calls):
    module = tmp_path / "subject.py"
    module.write_text(source)
    sys.modules.pop("subject", None)
    sys.path.insert(0, str(tmp_path))
    try:
        with Coverage(module) as cov:
            subject = __import__("subject")
            results = [getattr(subject, f)(*args) for f, args in calls]
    finally:
        sys.path.remove(str(tmp_path))
    return cov.report(), results


def test_ex3_and_ex7_coverage(tmp_path):
    days = (
        "MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)\n"
        "def is_leap(year):\n"
        "    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n"
        "def days_in_month(year, month):\n"
        "    if month == 2 and is_leap(year):\n"
        "        return 29\n"
        "    return MONTH_DAYS[month - 1]\n"
    )
    two = [("days_in_month", (2024, 2)), ("days_in_month", (2026, 1))]
    report, _ = coverage_of(tmp_path, days, two)
    assert report["missed lines"] == [] and 5 in report["missed branches at lines"]
    report, _ = coverage_of(tmp_path, days, [*two, ("days_in_month", (2026, 2))])
    assert 5 not in report["missed branches at lines"]
    wrong = "def is_leap(year):\n    return year % 4 == 0 and year % 100 != 0\n"
    calls = [("is_leap", (y,)) for y in (2024, 2026, 1900)]
    report, results = coverage_of(tmp_path, wrong, calls)
    assert results == [True, False, False]  # the right answers: the suite passes
    assert (
        report["branches"][0] == report["branches"][1] and report["missed lines"] == []
    )
    assert towndate.is_leap(2000)  # ... and the wrong rule says 2000 is not


def test_problem_q20_which_new_test_kills_what():
    import towndate  # noqa: F401,F811

    path = LISTINGS / "towndate.py"
    no_boundaries = mutate.suite_of("date_tests", lambda n: n != "test_new_boundaries")
    results = mutate.analyse("towndate", path, no_boundaries)
    survivors = [r[:3] for r in results if not r[3]]
    assert len(survivors) == 6  # the calendar test alone kills all of lines 17 and 33
    assert {line for line, _, _ in survivors} == {4, 27, 42}
    assert [r for r in survivors if r[0] == 4] == [(4, "31", "32")]  # December only

// library_test.cpp: dates, the three policies, and the fines on the town's loans.
#include <cassert>
#include <chrono>
#include <cstdio>
#include "library.hpp"
#include "../exercises/capped.hpp"

static int chrono_days(const std::string &iso)      // an independent date computation
{
    using namespace std::chrono;
    year_month_day ymd{year{std::stoi(iso.substr(0, 4))}, month{unsigned(std::stoi(iso.substr(5, 2)))},
                       day{unsigned(std::stoi(iso.substr(8, 2)))}};
    return int(sys_days{ymd}.time_since_epoch().count());
}

int main()
{
    assert(day_number("1970-01-01") == 0);
    assert(day_number("2000-03-01") == 11017);
    for (const char *d : {"2024-02-29", "2025-01-01", "2025-03-01", "2025-12-31", "1999-12-31"})
        assert(day_number(d) == chrono_days(d));

    StandardFine s;
    ComicFine c;
    StudyFine st;
    assert(s.fine_cents(1) == 10 && s.fine_cents(50) == 500 && s.fine_cents(200) == 500);
    assert(c.fine_cents(1) == 25 && c.fine_cents(12) == 300 && c.fine_cents(13) == 300);
    assert(st.fine_cents(3) == 0 && st.fine_cents(4) == 20 && st.fine_cents(100) == 1940);

    auto books = read_books("../../../../data/town/books.csv");
    auto loans = read_loans("../../../../data/town/loans.csv");
    assert(books.size() == 80 && loans.size() == 400);
    for (const auto &r : read_csv("../../../../data/town/loans.csv")) {
        assert(day_number(r[3]) == chrono_days(r[3]));
        assert(day_number(r[4]) - day_number(r[3]) == 21);     // due 21 days after
    }
    int today = day_number("2025-12-31");
    int total = 0, late = 0, by_policy[3] = {0, 0, 0};
    for (const Loan &l : loans) {
        int d = days_late(l, today);
        const Book &b = books.at(l.book_id);
        int expect = 0;                                         // the rules, written again directly
        if (d > 0) {
            late++;
            if (b.genre == "comics") expect = std::min(25 * d, 300);
            else if (b.genre == "science" || b.genre == "history") expect = d > 3 ? 20 * (d - 3) : 0;
            else expect = std::min(10 * d, 500);
        }
        int got = d > 0 ? policy_for(b).fine_cents(d) : 0;
        assert(got == expect);
        total += got;
        by_policy[b.genre == "comics" ? 1 : (b.genre == "science" || b.genre == "history") ? 2 : 0] += got;
    }
    assert(late == 109);
    assert(by_policy[0] == 11410 && by_policy[1] == 5175 && by_policy[2] == 29760);
    assert(total == 11410 + 5175 + 29760);
    // exercise 9: capping never raises a fine, and a cap above every fine changes nothing
    assert(total_capped(books, loans, today, 1000000) == total);
    assert(total_capped(books, loans, today, 1000) == 30905);    // quoted in the solution
    assert(total_capped(books, loans, today, 0) == 0);
    std::printf("library_test: OK (total %d cents, capped at 10.00: %d)\n", total,
                total_capped(books, loans, today, 1000));
    return 0;
}

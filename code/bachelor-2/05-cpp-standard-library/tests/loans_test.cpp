// loans_test.cpp: reading the loans, grouping by member and by month (exercise 7).
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <map>
#include "loans.hpp"
#include "../exercises/by_month.hpp"
#include "../exercises/loan_desk.hpp"

int main()
{
    assert(day_number("1970-01-01") == 0 && day_number("2025-01-01") == 20089);
    for (int d = day_number("2024-01-01"); d <= day_number("2026-12-31"); d++)
        assert(month_of(d) >= 1 && month_of(d) <= 12);
    assert(month_of(day_number("2024-02-29")) == 2 && month_of(day_number("2025-12-31")) == 12);
    assert(month_of(day_number("2025-03-01")) == 3 && month_of(day_number("2025-01-31")) == 1);

    auto loans = read_loans("../../../../data/town/loans.csv");
    assert(loans.size() == 400 && loans[0].returned == day_number("2025-01-03"));
    int today = day_number("2025-12-31"), late = 0, out = 0;
    for (const Loan &l : loans) {
        late += is_late(l, today);
        out += l.returned < 0;
    }
    assert(late == 109 && out == 22);

    std::map<int, int> per_member;
    for (const Loan &l : loans)
        per_member[l.member_id]++;
    assert(per_member.size() == 60 && per_member[55] == 12 && per_member[14] == 11);

    auto table = loans_by_member_month(loans);
    int sum = 0;
    for (const auto &[member, months] : table) {
        int s = 0;
        for (const auto &[m, n] : months)
            s += n;
        assert(s == per_member[member]);            // the months of a member add up to the member's loans
        sum += s;
    }
    assert(sum == 400 && table.size() == 60);
    std::vector<Loan> sorted = loans;               // the weekend problem
    sort_by_due(sorted);
    assert(std::is_sorted(sorted.begin(), sorted.end(), [](const Loan &a, const Loan &b) { return a.due < b.due; }));
    for (int d = day_number("2025-01-01"); d < day_number("2026-01-31"); d += 3) {
        auto [first, last] = due_between(sorted, d, d + 7);
        long by_hand = std::count_if(loans.begin(), loans.end(), [d](const Loan &l) { return l.due >= d && l.due < d + 7; });
        assert(last - first == by_hand);
        for (auto it = first; it != last; ++it)
            assert(it->due >= d && it->due < d + 7);
    }
    long by_hand = 0, cents = 0;                    // question 18: the count, by a loop written by hand
    for (const Loan &l : loans) {
        int end = l.returned >= 0 ? l.returned : today;
        by_hand += end > l.due;
        cents += end > l.due ? 10 * (end - l.due) : 0;
    }
    assert(late_count(loans, today) == by_hand && by_hand == 109 && fines_cents(loans, today) == cents);
    std::printf("fines %ld cents\n", cents);
    std::puts("loans_test: OK");
    return 0;
}

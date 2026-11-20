// loan_desk.hpp: the loan desk of the weekend problem, Parts I and III.
#pragma once
#include <algorithm>
#include <numeric>
#include <utility>
#include <vector>
#include "../listings/loans.hpp"

inline void sort_by_due(std::vector<Loan> &loans)                     // question 1
{
    std::sort(loans.begin(), loans.end(), [](const Loan &a, const Loan &b) {
        return a.due != b.due ? a.due < b.due : a.id < b.id;
    });
}

struct DueBefore {                                                    // compares a loan with a day, both ways
    bool operator()(const Loan &l, int day) const { return l.due < day; }
    bool operator()(int day, const Loan &l) const { return day < l.due; }
};

// questions 2 and 4: the loans due in [from, to), as an iterator range of a vector sorted by due date
inline std::pair<std::vector<Loan>::const_iterator, std::vector<Loan>::const_iterator>
due_between(const std::vector<Loan> &sorted, int from, int to)
{
    return {std::lower_bound(sorted.begin(), sorted.end(), from, DueBefore{}),
            std::lower_bound(sorted.begin(), sorted.end(), to, DueBefore{})};
}

inline long late_count(const std::vector<Loan> &loans, int today)    // question 13
{
    return std::count_if(loans.begin(), loans.end(), [today](const Loan &l) { return is_late(l, today); });
}

inline long fines_cents(const std::vector<Loan> &loans, int today)   // question 17: 10 cents per day late
{
    return std::transform_reduce(loans.begin(), loans.end(), 0L, std::plus<>(), [today](const Loan &l) {
        int end = l.returned >= 0 ? l.returned : today;
        return end > l.due ? 10L * (end - l.due) : 0L;
    });
}

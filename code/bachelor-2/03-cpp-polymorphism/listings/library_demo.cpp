// library_demo.cpp: the fines owed on the town's loans at the end of 2025.
#include <algorithm>
#include <cstdio>
#include "library.hpp"

int main(int argc, char **argv)
{
    if (argc != 3) {
        std::fprintf(stderr, "usage: library_demo books.csv loans.csv\n");
        return 2;
    }
    auto books = read_books(argv[1]);
    auto loans = read_loans(argv[2]);
    int today = day_number("2025-12-31");
    std::map<std::string, std::pair<int, int>> per_policy;     // name -> (late loans, cents)
    std::vector<std::pair<int, int>> fines;                    // (cents, loan id)
    for (const Loan &l : loans) {
        int d = days_late(l, today);
        if (d == 0)
            continue;
        const FinePolicy &p = policy_for(books.at(l.book_id)); // dynamic dispatch from here on
        int c = p.fine_cents(d);
        per_policy[p.name()].first++;
        per_policy[p.name()].second += c;
        fines.push_back({c, l.id});
    }
    std::printf("%zu loans, %zu late\n", loans.size(), fines.size());
    for (const auto &[name, v] : per_policy)
        std::printf("  %-9s %3d late loans, %7.2f owed\n", name.c_str(), v.first, v.second / 100.0);
    std::sort(fines.rbegin(), fines.rend());
    for (int i = 0; i < 3; i++)
        std::printf("  largest: loan %d, %.2f\n", fines[i].second, fines[i].first / 100.0);
    return 0;
}

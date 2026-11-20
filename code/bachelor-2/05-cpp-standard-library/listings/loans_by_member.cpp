// loans_by_member.cpp: the town's loans grouped by member, with a map from member to loans.
#include <algorithm>
#include <cstdio>
#include <map>
#include <vector>
#include "loans.hpp"

int main(int argc, char **argv)
{
    std::vector<Loan> loans = read_loans(argc > 1 ? argv[1] : "loans.csv");
    std::map<int, std::vector<Loan>> by_member;              // member -> that member's loans
    for (const Loan &l : loans)
        by_member[l.member_id].push_back(l);                 // [] creates an empty vector
    std::vector<std::pair<int, int>> counts;                 // (member, number of loans)
    for (const auto &[member, list] : by_member)
        counts.emplace_back(member, int(list.size()));
    std::stable_sort(counts.begin(), counts.end(),
                     [](auto a, auto b) { return a.second > b.second; });
    int today = day_number("2025-12-31");
    std::printf("%zu loans, %zu members who borrowed\n", loans.size(), by_member.size());
    std::printf("member  loans  late\n");
    for (int i = 0; i < 5; i++) {
        const auto &list = by_member.at(counts[i].first);  // at() throws if the key is missing
        auto late_now = [today](const Loan &l) { return is_late(l, today); };
        auto late = std::count_if(list.begin(), list.end(), late_now);
        std::printf("%6d %6d %5ld\n", counts[i].first, counts[i].second, late);
    }
    return 0;
}

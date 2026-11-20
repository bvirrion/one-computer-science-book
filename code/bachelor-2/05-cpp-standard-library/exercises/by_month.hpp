// by_month.hpp: loans grouped by member, then by month of the loan (exercise 7).
#pragma once
#include <map>
#include <string>
#include <vector>
#include "../listings/loans.hpp"

inline int month_of(int day)                        // 1..12, from a day number (inverse of day_number)
{
    int z = day + 719468, era = (z >= 0 ? z : z - 146096) / 146097;
    int doe = z - era * 146097;
    int yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    int doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    int mp = (5 * doy + 2) / 153;
    return mp < 10 ? mp + 3 : mp - 9;
}

// member -> month -> number of loans taken out that month
inline std::map<int, std::map<int, int>> loans_by_member_month(const std::vector<Loan> &loans)
{
    std::map<int, std::map<int, int>> table;
    for (const Loan &l : loans)
        table[l.member_id][month_of(l.out)]++;
    return table;
}

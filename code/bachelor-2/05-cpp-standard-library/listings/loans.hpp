// loans.hpp: the town library's loans, read from loans.csv (no quoted fields).
#pragma once
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

inline int day_number(const std::string &iso)     // days since 1970-01-01 of "YYYY-MM-DD"
{
    int y = std::stoi(iso.substr(0, 4)), m = std::stoi(iso.substr(5, 2)), d = std::stoi(iso.substr(8, 2));
    y -= m <= 2;                                    // count the year from March
    int era = y / 400, yoe = y - era * 400;
    int doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    return era * 146097 + yoe * 365 + yoe / 4 - yoe / 100 + doy - 719468;
}

struct Loan { int id, book_id, member_id, out, due, returned; };   // returned = -1: still out

inline std::vector<Loan> read_loans(const std::string &path)
{
    std::ifstream in(path);
    if (!in)
        throw std::runtime_error("cannot open " + path);
    std::vector<Loan> loans;
    std::string line, f[6];
    std::getline(in, line);                         // the header
    while (std::getline(in, line)) {
        std::istringstream fields(line);
        for (auto &x : f)
            if (!std::getline(fields, x, ','))
                x.clear();                          // an empty last field
        loans.push_back({std::stoi(f[0]), std::stoi(f[1]), std::stoi(f[2]), day_number(f[3]),
                         day_number(f[4]), f[5].empty() ? -1 : day_number(f[5])});
    }
    return loans;
}

inline bool is_late(const Loan &l, int today)       // returned after the due date, or still out and overdue
{
    return l.returned >= 0 ? l.returned > l.due : today > l.due;
}

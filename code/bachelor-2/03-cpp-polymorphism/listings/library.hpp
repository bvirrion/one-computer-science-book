// library.hpp: the town library's loans and its fine policies, one class per policy.
#pragma once
#include <fstream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

int day_number(const std::string &iso)            // days since 1970-01-01 of "YYYY-MM-DD"
{
    int y = std::stoi(iso.substr(0, 4)), m = std::stoi(iso.substr(5, 2)), d = std::stoi(iso.substr(8, 2));
    y -= m <= 2;                                    // count the year from March
    int era = y / 400, yoe = y - era * 400;
    int doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    return era * 146097 + yoe * 365 + yoe / 4 - yoe / 100 + doy - 719468;
}

struct Book { int id; std::string title, genre; };
struct Loan { int id, book_id, member_id, out, due, returned; };   // returned = -1: still out

std::vector<std::vector<std::string>> read_csv(const std::string &path)   // no quoted fields
{
    std::ifstream in(path);
    if (!in)
        throw std::runtime_error("cannot open " + path);
    std::vector<std::vector<std::string>> rows;
    std::string line, field;
    std::getline(in, line);                         // the header
    while (std::getline(in, line)) {
        std::vector<std::string> row;
        std::istringstream fields(line);
        while (std::getline(fields, field, ','))
            row.push_back(field);
        if (line.back() == ',')
            row.push_back("");                      // an empty last field
        rows.push_back(row);
    }
    return rows;
}

std::map<int, Book> read_books(const std::string &path)
{
    std::map<int, Book> books;
    for (const auto &r : read_csv(path))
        books[std::stoi(r[0])] = Book{std::stoi(r[0]), r[1], r[4]};
    return books;
}

std::vector<Loan> read_loans(const std::string &path)
{
    std::vector<Loan> loans;
    for (const auto &r : read_csv(path))
        loans.push_back({std::stoi(r[0]), std::stoi(r[1]), std::stoi(r[2]), day_number(r[3]),
                         day_number(r[4]), r[5].empty() ? -1 : day_number(r[5])});
    return loans;
}

int days_late(const Loan &l, int today)             // late days so far, 0 if on time
{
    int end = l.returned >= 0 ? l.returned : today;
    return end > l.due ? end - l.due : 0;
}

class FinePolicy {                              // an abstract class: the interface of a policy
public:
    virtual ~FinePolicy() = default;
    virtual int fine_cents(int days_late) const = 0;
    virtual std::string name() const = 0;
};

class StandardFine : public FinePolicy {            // 10 cents a day, at most 5.00
public:
    int fine_cents(int d) const override { return d * 10 < 500 ? d * 10 : 500; }
    std::string name() const override { return "standard"; }
};

class ComicFine : public FinePolicy {               // 25 cents a day, at most 3.00
public:
    int fine_cents(int d) const override { return d * 25 < 300 ? d * 25 : 300; }
    std::string name() const override { return "comic"; }
};

class StudyFine : public FinePolicy {               // 3 days of grace, then 20 cents a day
public:
    int fine_cents(int d) const override { return d > 3 ? (d - 3) * 20 : 0; }
    std::string name() const override { return "study"; }
};

const FinePolicy &policy_for(const Book &b)         // the only place that knows the genres
{
    static const StandardFine standard;
    static const ComicFine comic;
    static const StudyFine study;
    if (b.genre == "comics")
        return comic;
    if (b.genre == "science" || b.genre == "history")
        return study;
    return standard;
}

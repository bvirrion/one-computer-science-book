// capped.hpp (exercise 9): a policy that caps another policy, by composition.
#pragma once
#include <string>
#include "library.hpp"

class CappedFine : public FinePolicy {
public:
    CappedFine(const FinePolicy &inner, int cap_cents) : inner_(inner), cap_(cap_cents) {}
    int fine_cents(int d) const override
    {
        int f = inner_.fine_cents(d);
        return f < cap_ ? f : cap_;
    }
    std::string name() const override { return inner_.name() + " capped"; }

private:
    const FinePolicy &inner_;                       // has a policy; is not one of the three
    int cap_;
};

// Total owed on all loans when every policy is capped at cap_cents.
int total_capped(const std::map<int, Book> &books, const std::vector<Loan> &loans, int today, int cap_cents)
{
    int total = 0;
    for (const Loan &l : loans) {
        int d = days_late(l, today);
        if (d > 0)
            total += CappedFine(policy_for(books.at(l.book_id)), cap_cents).fine_cents(d);
    }
    return total;
}

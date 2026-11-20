// fraction.hpp: a class whose constructor establishes an invariant.
#pragma once
#include <numeric>
#include <stdexcept>

class Fraction {
public:
    // Invariant: den_ > 0 and gcd(num_, den_) == 1.
    Fraction(long num, long den) : num_(num), den_(den)
    {
        if (den_ == 0)
            throw std::invalid_argument("zero denominator");
        if (den_ < 0) {
            num_ = -num_;
            den_ = -den_;
        }
        long g = std::gcd(num_, den_);
        num_ /= g;
        den_ /= g;
    }
    Fraction(long whole) : Fraction(whole, 1) {}

    long num() const { return num_; }
    long den() const { return den_; }
    Fraction operator+(const Fraction &o) const
    {
        return Fraction(num_ * o.den_ + o.num_ * den_, den_ * o.den_);
    }
    Fraction operator*(const Fraction &o) const
    {
        return Fraction(num_ * o.num_, den_ * o.den_);
    }
    bool operator==(const Fraction &o) const = default;

private:
    long num_;
    long den_;
};

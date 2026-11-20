// clamp.hpp (exercise 3): clamp a value into [lo, hi], for any totally ordered type.
#pragma once
#include <concepts>
#include <stdexcept>

template <typename T>
concept TotallyOrdered = requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};

template <TotallyOrdered T>
const T &clamp_to(const T &x, const T &lo, const T &hi)
{
    if (hi < lo)
        throw std::invalid_argument("clamp_to: hi < lo");
    if (x < lo) return lo;
    if (hi < x) return hi;
    return x;
}

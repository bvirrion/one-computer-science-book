// bsearch.hpp (exercise 7): binary search over any sorted random-access range.
#pragma once
#include <iterator>

// Returns the first position p in [first, last) with !(*p < key), or last.
template <std::random_access_iterator It, typename K>
    requires requires(It p, const K &k) { { *p < k } -> std::convertible_to<bool>; }
It lower_bound_of(It first, It last, const K &key)
{
    auto n = last - first;                  // invariant: the answer lies in [first, first + n]
    while (n > 0) {
        auto half = n / 2;
        It mid = first + half;
        if (*mid < key) {
            first = mid + 1;
            n -= half + 1;
        } else {
            n = half;
        }
    }
    return first;
}

template <std::random_access_iterator It, typename K>
bool contains(It first, It last, const K &key)
{
    It p = lower_bound_of(first, last, key);
    return p != last && !(key < *p);
}

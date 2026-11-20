// counting_test.cpp: exact copy and move counts of a growing vector (r = 2 in libstdc++).
#include <cassert>
#include <cstdio>
#include <vector>
#include "tracked.hpp"

template <class T> void check(int n, bool nothrow_move)
{
    counts = Counts{};
    std::vector<T> v;
    long transfers = 0;                        // elements carried over at each regrowth
    for (int i = 0; i < n; i++) {
        if (v.size() == v.capacity())          // full: this push regrows
            transfers += long(v.size());
        v.push_back(T(i));
    }
    // the proposition with r = 2: fewer than r(n-1)/(r-1) = 2(n-1) transfers
    if (n >= 2)
        assert(transfers < 2L * (n - 1));
    if (nothrow_move) {
        assert(counts.copies == 0);
        assert(counts.moves == n + transfers);
    } else {
        assert(counts.copies == transfers);
        assert(counts.moves == n);
    }
    for (int i = 0; i < n; i++)
        assert(v[std::size_t(i)].value() == i);
}

int main()
{
    for (int n = 0; n <= 5000; n++) {
        check<Tracked>(n, true);
        check<TrackedMayThrow>(n, false);
    }
    // the hook's claim: returning a local vector moves nothing
    counts = Counts{};
    auto make = [] { std::vector<Tracked> v; v.reserve(100); for (int i = 0; i < 100; i++) v.emplace_back(i); return v; };
    std::vector<Tracked> r = make();
    assert(counts.copies == 0 && counts.moves == 0 && r.size() == 100);
    std::puts("counting_test: OK");
    return 0;
}

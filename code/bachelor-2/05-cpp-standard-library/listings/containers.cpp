// containers.cpp: four sequence containers, the same four values, four layouts.
#include <array>
#include <cstdio>
#include <deque>
#include <list>
#include <vector>

template <class C> long gap(const C &c)            // bytes between the first two elements
{
    auto first = c.begin(), second = std::next(c.begin());
    return reinterpret_cast<const char *>(&*second) - reinterpret_cast<const char *>(&*first);
}

int main()
{
    std::array<int, 4> a{1, 2, 3, 4};
    std::vector<int> v{1, 2, 3, 4};
    std::deque<int> d{1, 2, 3, 4};
    std::list<int> l{1, 2, 3, 4};
    std::printf("%-6s %7s %16s\n", "", "sizeof", "1st to 2nd");
    std::printf("%-6s %7zu %16ld\n", "array", sizeof a, gap(a));
    std::printf("%-6s %7zu %16ld\n", "vector", sizeof v, gap(v));
    std::printf("%-6s %7zu %16ld\n", "deque", sizeof d, gap(d));
    std::printf("%-6s %7zu %16ld\n", "list", sizeof l, gap(l));
    d.push_front(0);                                // constant time: deque and list only
    l.push_front(0);
    v.insert(v.begin(), 0);                         // allowed, but moves every element
    std::printf("front %d %d %d, size %zu %zu %zu\n", d.front(), l.front(), v.front(),
        d.size(), l.size(),
                v.size());
    return 0;
}

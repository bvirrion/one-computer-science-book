// exo_count.cpp (exercise 1): how many copies and moves?
#include <cstdio>
#include <utility>
#include <vector>
#include "tracked.hpp"

Tracked pass(Tracked t) { return t; }

int main()
{
    Tracked a(1);
    Tracked b = a;                              // line A
    Tracked c = std::move(a);                   // line B
    b = c;                                      // line C
    Tracked d = pass(b);                        // line D
    std::vector<Tracked> v;
    v.reserve(4);
    v.push_back(d);                             // line E
    v.push_back(Tracked(5));                    // line F
    std::printf("%ld copies, %ld moves\n", counts.copies, counts.moves);
    return 0;
}

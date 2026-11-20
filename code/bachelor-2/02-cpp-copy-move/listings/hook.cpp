// hook.cpp: a function returns a vector of a million values. Is it copied?
#include <cstdio>
#include <vector>
#include "tracked.hpp"

const Tracked *seen = nullptr;          // where the elements lived inside the function

std::vector<Tracked> make_readings(int n)
{
    std::vector<Tracked> v;
    v.reserve(n);
    for (int i = 0; i < n; i++)
        v.emplace_back(i);              // built in place: no copy, no move
    seen = v.data();
    return v;
}

int main()
{
    std::vector<Tracked> r = make_readings(1000000);
    std::printf("returned:  %ld copies, %ld moves, same elements: %s\n",
                counts.copies, counts.moves, r.data() == seen ? "yes" : "no");
    std::vector<Tracked> backup = r;    // now ask for a copy
    std::printf("backup:    %ld copies, %ld moves\n", counts.copies, counts.moves);
    return 0;
}

// growth.cpp: what a vector does with its elements when it grows.
#include <cstdio>
#include <vector>
#include "tracked.hpp"

template <class T> void fill(const char *name, int n)
{
    counts = Counts{};
    std::vector<T> v;
    std::size_t cap = v.capacity(), regrowths = 0;
    for (int i = 0; i < n; i++) {
        v.push_back(T(i));               // the temporary T(i) is moved in
        if (v.capacity() != cap) {
            regrowths++;
            cap = v.capacity();
        }
    }
    std::printf("%-16s n=%d: %2zu regrowths, capacity %zu, %ld copies, %ld moves\n",
                name, n, regrowths, cap, counts.copies, counts.moves);
}

int main()
{
    for (int n : {1000, 1025}) {
        fill<Tracked>("noexcept move", n);
        fill<TrackedMayThrow>("move may throw", n);
    }
    return 0;
}

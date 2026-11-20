// exercises_test.cpp: the interval map (exercise 10) and the three queues (exercise 12).
#include <cassert>
#include <cstdio>
#include <random>
#include <vector>
#include "../exercises/interval_map.hpp"
#include "../exercises/workload.hpp"

int main()
{
    IntervalMap<char> m('A');
    m.assign(3, 7, 'B');
    m.assign(5, 9, 'C');
    assert(m[2] == 'A' && m[3] == 'B' && m[4] == 'B' && m[5] == 'C' && m[8] == 'C' && m[9] == 'A');
    m.assign(0, 20, 'A');
    assert(m.changes() == 0);                       // back to a single value: nothing stored

    std::mt19937 gen(11);
    IntervalMap<int> im(0);
    std::vector<int> ref(60, 0);                    // the keys -10..49, by brute force
    for (int step = 0; step < 3000; step++) {
        int lo = int(gen() % 60) - 10, hi = int(gen() % 60) - 10, v = int(gen() % 3);
        im.assign(lo, hi, v);
        for (int k = lo; k < hi; k++)
            ref[std::size_t(k + 10)] = v;
        std::size_t runs = 0;                       // the number of changes the canonical form needs
        for (int k = -10; k < 50; k++) {
            assert(im[k] == ref[std::size_t(k + 10)]);
            int before = k == -10 ? 0 : ref[std::size_t(k + 9)];
            runs += ref[std::size_t(k + 10)] != before;
        }
        runs += ref[59] != 0;                       // the change back to 0 at 50
        assert(im.changes() == runs);
        assert(im[-100] == 0 && im[1000] == 0);
    }

    std::vector<int> ops;
    for (int i = 0; i < 3000; i++)
        ops.push_back(gen() % 3 ? int(gen() % 500) : -1);
    auto a = run<HeapQueue>(ops), b = run<SetQueue>(ops), c = run<SortedVectorQueue>(ops);
    assert(a == b && b == c && !a.empty());         // the same members served in the same order
    std::puts("exercises_test: OK");
    return 0;
}

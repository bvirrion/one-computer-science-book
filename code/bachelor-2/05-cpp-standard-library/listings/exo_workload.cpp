// exo_workload.cpp: the three queues of exercise 12 on the same random stream, for growing queue sizes.
#include <chrono>
#include <cstdio>
#include <random>
#include "../exercises/workload.hpp"

template <class Q> double ms(const std::vector<int> &ops, std::vector<int> &out)
{
    auto t0 = std::chrono::steady_clock::now();
    out = run<Q>(ops);
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main()
{
    std::mt19937 gen(2025);
    std::printf("%8s %8s %8s %14s\n", "waiting", "heap ms", "set ms", "sorted vec ms");
    for (int w : {100, 1000, 10000, 100000}) {
        std::vector<int> ops;
        for (int i = 0; i < w; i++) ops.push_back(int(gen() % 1000000));   // w members waiting
        for (int i = 0; i < 200000; i++) {                                // then serve one, add one
            ops.push_back(-1);
            ops.push_back(int(gen() % 1000000));
        }
        std::vector<int> a, b, c;
        double th = ms<HeapQueue>(ops, a), ts = ms<SetQueue>(ops, b), tv = ms<SortedVectorQueue>(ops, c);
        if (a != b || b != c) return 1;                                   // same order of service
        std::printf("%8d %8.1f %8.1f %14.1f\n", w, th, ts, tv);
    }
    return 0;
}

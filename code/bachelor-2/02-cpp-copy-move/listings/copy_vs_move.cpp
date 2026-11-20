// copy_vs_move.cpp: time to hand over a vector of n doubles, by copy and by move.
#include <chrono>
#include <cstdio>
#include <utility>
#include <vector>

template <class F> double ns(F f, int reps)
{
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < reps; i++)
        f();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::nano>(t1 - t0).count() / reps;
}

int main()
{
    std::printf("%10s %14s %12s\n", "n", "copy (ns)", "move (ns)");
    for (int n = 1000; n <= 10000000; n *= 10) {
        std::vector<double> src(n, 1.5), dst;
        int reps = n >= 1000000 ? 20 : 2000;
        double c = ns([&] { dst = src; }, reps);   // dst already has room after the first copy
        std::vector<double>().swap(dst);                   // free dst before timing the moves
        double m = ns([&] { dst = std::move(src); src = std::move(dst); }, reps) / 2;
        std::printf("%10d %14.0f %12.1f\n", n, c, m);
    }
    return 0;
}

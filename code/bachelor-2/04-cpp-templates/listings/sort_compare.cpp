// sort_compare.cpp: qsort with a comparison through a pointer, std::sort with an inlined one.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

int compare_ints(const void *a, const void *b)       // what qsort calls, n log n times
{
    int x = *static_cast<const int *>(a), y = *static_cast<const int *>(b);
    return (x > y) - (x < y);
}

template <class F> double ms(F f)
{
    auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main()
{
    std::mt19937 gen(2025);
    std::printf("%10s %10s %12s %8s\n", "n", "qsort ms", "std::sort ms", "ratio");
    for (int n = 10000; n <= 10000000; n *= 10) {
        std::vector<int> a(n);
        for (int &x : a) x = int(gen());
        std::vector<int> b = a;
        double q = ms([&] { std::qsort(a.data(), a.size(), sizeof(int), compare_ints); });
        double s = ms([&] { std::sort(b.begin(), b.end(),
            [](int x, int y) { return x < y; }); });
        if (a != b) return 1;                        // both sorted the same values
        std::printf("%10d %10.2f %12.2f %8.1f\n", n, q, s, q / s);
    }
    return 0;
}

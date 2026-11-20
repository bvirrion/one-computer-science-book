// exception_cost.cpp: what a failure costs, reported by a return code or by a throw.
#include <chrono>
#include <iostream>
#include <stdexcept>

__attribute__((noinline)) int check_code(int x) { return x < 0 ? -1 : x; }
__attribute__((noinline)) int check_throw(int x)
{
    if (x < 0)
        throw std::domain_error("negative");
    return x;
}

template <class F> double ns_per_call(F f, int calls)
{
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < calls; i++)
        f(i);
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::nano>(t1 - t0).count() / calls;
}

int main()
{
    const int n = 1'000'000;
    volatile long sink = 0;
    double ok_code = ns_per_call([&](int i) { sink = sink + check_code(i); }, n);
    double ok_throw = ns_per_call([&](int i) { sink = sink + check_throw(i); }, n);
    double bad_code = ns_per_call([&](int i) {
        if (check_code(-i - 1) < 0) sink = sink + 1; }, n);
    double bad_throw = ns_per_call([&](int i) {
        try { sink = sink + check_throw(-i - 1); } catch (const std::domain_error &) { sink = sink + 1; }
    }, n);
    std::cout.precision(3);
    std::cout << "success, return code: " << ok_code << " ns per call\n";
    std::cout << "success, may throw:   " << ok_throw << " ns per call\n";
    std::cout << "failure, return code: " << bad_code << " ns per call\n";
    std::cout << "failure, throw/catch: " << bad_throw << " ns per call\n";
    std::cout << "a throw costs about " << static_cast<long>(bad_throw / bad_code)
              << " failed return codes\n";
    return 0;
}

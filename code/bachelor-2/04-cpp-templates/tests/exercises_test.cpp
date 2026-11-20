// exercises_test.cpp: clamp (3), binary search (7), matrices (9), heap (10), binomials (12).
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <random>
#include <string>
#include <vector>
#include "../exercises/binomial.hpp"
#include "../exercises/bsearch.hpp"
#include "../exercises/clamp.hpp"
#include "../exercises/heap.hpp"
#include "../exercises/matrix.hpp"

template <typename A, typename B> concept Multipliable = requires(A a, B b) { a * b; };
template <typename T> concept Clampable = requires(const T &x) { clamp_to(x, x, x); };
struct Opaque {};

int main()
{
    assert(clamp_to(5, 0, 3) == 3 && clamp_to(-1, 0, 3) == 0 && clamp_to(2, 0, 3) == 2);
    assert(clamp_to(std::string("m"), std::string("a"), std::string("f")) == "f");
    static_assert(Clampable<double> && !Clampable<Opaque>);                 // refused by the concept

    std::mt19937 gen(4);
    for (int trial = 0; trial < 200; trial++) {
        std::vector<int> v(gen() % 50);
        for (int &x : v) x = int(gen() % 40);
        std::sort(v.begin(), v.end());
        for (int key = -1; key <= 41; key++) {
            assert(lower_bound_of(v.begin(), v.end(), key) == std::lower_bound(v.begin(), v.end(), key));
            assert(contains(v.begin(), v.end(), key) == std::binary_search(v.begin(), v.end(), key));
        }
    }

    Matrix<int, 2, 3> m;
    for (std::size_t i = 0; i < 2; i++)
        for (std::size_t j = 0; j < 3; j++) m(i, j) = int(i * 3 + j);
    Matrix<int, 2, 2> g = m * transpose(m);
    assert(g(0, 0) == 5 && g(0, 1) == 14 && g(1, 1) == 50);
    static_assert(Multipliable<Matrix<int, 2, 3>, Matrix<int, 3, 4>>);
    static_assert(!Multipliable<Matrix<int, 2, 3>, Matrix<int, 2, 3>>);     // refused at compile time

    Heap<int> h;
    std::vector<int> all;
    for (int i = 0; i < 500; i++) { int x = int(gen() % 1000); h.push(x); all.push_back(x); }
    std::sort(all.rbegin(), all.rend());
    for (int x : all) { assert(h.top() == x); h.pop(); }
    assert(h.empty());
    Heap<std::string, std::greater<std::string>> words;                     // a min-heap
    for (const char *w : {"quay", "mill", "pier", "dunes"}) words.push(w);
    assert(words.top() == "dunes");

    for (std::size_t n = 1; n <= 67; n++)
        for (std::size_t k = 1; k < n; k++) assert(BINOM[n][k] == BINOM[n - 1][k - 1] + BINOM[n - 1][k]);
    std::uint64_t row = 0;
    for (std::size_t k = 0; k <= 20; k++) row += BINOM[20][k];
    assert(row == (1u << 20));
    std::puts("exercises_test: OK");
    return 0;
}

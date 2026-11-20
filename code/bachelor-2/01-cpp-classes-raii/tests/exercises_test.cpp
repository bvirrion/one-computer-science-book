// exercises_test.cpp: the solutions of exercises 3, 6, 7, 9, 10 and 12.
#include <cassert>
#include <cstdio>
#include <stdexcept>
#include <string>
#include "../exercises/bounded_stack.hpp"
#include "../exercises/int_array.hpp"
#include "../exercises/matrix.hpp"
#include "../exercises/merger.hpp"
#include "../exercises/scope_guard.hpp"
#include "../exercises/txn_file.hpp"
#include "open_files.hpp"

struct Fragile {                 // its copy throws when asked to
    static inline bool fail = false;
    int v;
    explicit Fragile(int x) : v(x) {}
    Fragile(const Fragile &o) : v(o.v)
    {
        if (fail)
            throw std::runtime_error("copy failed");
    }
};

static bool exists(const char *p)
{
    std::FILE *f = std::fopen(p, "r");
    if (f) std::fclose(f);
    return f != nullptr;
}

template <class E, class F> static bool throws(F f)
{
    try { f(); } catch (const E &) { return true; }
    return false;
}

int main()
{
    // 3: IntArray
    IntArray a(5);
    assert(a.size() == 5 && a.at(4) == 0);
    a.at(2) = 7;
    const IntArray &ca = a;
    assert(ca.at(2) == 7);
    assert(throws<std::out_of_range>([&] { a.at(5); }));

    // 6: Merger leaks nothing when its second file is missing
    const int base = count_open_files();
    for (int i = 0; i < 10; i++)
        assert(throws<std::runtime_error>([] { Merger m("../listings/good.log", "missing.log"); }));
    { Merger ok("../listings/good.log", "../listings/bad.log"); assert(count_open_files() == base + 2); }
    assert(count_open_files() == base);

    // 7: ScopeGuard
    int runs = 0;
    { ScopeGuard g([&] { runs++; }); }
    { ScopeGuard g([&] { runs++; }); g.dismiss(); }
    assert(throws<std::logic_error>([&] { ScopeGuard g([&] { runs += 10; }); throw std::logic_error("x"); }));
    assert(runs == 11);

    // 9: BoundedStack, strong push
    BoundedStack<Fragile, 3> s;
    s.push(Fragile(1));
    s.push(Fragile(2));
    Fragile::fail = true;
    assert(throws<std::runtime_error>([&] { s.push(Fragile(3)); }));
    Fragile::fail = false;
    assert(s.size() == 2 && s.top().v == 2);
    s.push(Fragile(3));
    assert(throws<std::length_error>([&] { s.push(Fragile(4)); }));
    assert(s.size() == 3 && s.top().v == 3);
    s.pop(); s.pop(); s.pop();
    assert(throws<std::out_of_range>([&] { s.pop(); }));

    // 10: TxnFile
    const char *p = "txn_test.out";
    std::remove(p);
    assert(throws<std::logic_error>([&] { TxnFile t(p); t.write("half"); throw std::logic_error("x"); }));
    assert(!exists(p) && !exists("txn_test.out.tmp"));
    { TxnFile t(p); t.write("whole\n"); t.commit(); }
    assert(exists(p) && !exists("txn_test.out.tmp"));
    std::remove(p);
    assert(count_open_files() == base);

    // 12: Matrix keeps rows * cols == size
    assert(throws<std::invalid_argument>([] { Matrix m(0, 3); }));
    Matrix m(2, 3);
    for (std::size_t r = 0; r < 2; r++)
        for (std::size_t c = 0; c < 3; c++)
            m(r, c) = static_cast<double>(10 * r + c);
    Matrix t = m.transposed();
    assert(t.rows() == 3 && t.cols() == 2 && t(2, 1) == 12.0);
    Matrix q = m * t;                          // 2 x 2
    assert(q.rows() == 2 && q(0, 0) == 5.0 && q(1, 1) == 100.0 + 121.0 + 144.0);
    assert(throws<std::invalid_argument>([&] { m * m; }));
    assert(throws<std::out_of_range>([&] { m(2, 0); }));
    Matrix w(1, 1, 7.0);
    w = q;                                     // assignment keeps the invariant
    assert(w.rows() == 2 && w.cols() == 2 && w(1, 1) == q(1, 1));
    w = Matrix(3, 1, 2.0);
    assert(w.rows() == 3 && w(2, 0) == 2.0);
    std::puts("exercises_test: ok");
    return 0;
}

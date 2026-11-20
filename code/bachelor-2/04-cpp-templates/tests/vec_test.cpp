// vec_test.cpp: Vec<T> with several types, and its copies and moves counted.
#include <cassert>
#include <cstdio>
#include <memory>
#include <string>
#include "vec.hpp"

static long copies = 0, moves = 0, alive = 0;
struct Tracked {                                  // the counting type of chapter 2, copied here
    int v;
    explicit Tracked(int x) : v(x) { alive++; }
    Tracked(const Tracked &o) : v(o.v) { copies++; alive++; }
    Tracked(Tracked &&o) noexcept : v(o.v) { moves++; alive++; }
    Tracked &operator=(const Tracked &o) { v = o.v; copies++; return *this; }
    Tracked &operator=(Tracked &&o) noexcept { v = o.v; moves++; return *this; }
    ~Tracked() { alive--; }
};

struct Fragile {                                  // copies may throw; no noexcept move
    static inline int budget = 1000000;
    int v;
    explicit Fragile(int x) : v(x) {}
    Fragile(const Fragile &o) : v(o.v) { if (--budget < 0) throw std::runtime_error("copy failed"); }
};

int main()
{
    {
        Vec<int> a;
        for (int i = 0; i < 1000; i++) a.push_back(i);
        assert(a.size() == 1000 && a.capacity() == 1024 && a[999] == 999);
        long sum = 0;
        for (int x : a) sum += x;
        assert(sum == 999L * 1000 / 2);
        bool threw = false;
        try { a.at(1000); } catch (const std::out_of_range &) { threw = true; }
        assert(threw);
    }
    {
        Vec<std::string> s;
        s.push_back("a long street name that does not fit in a small string");
        Vec<std::string> t = s;
        t[0][0] = 'A';
        assert(s[0][0] == 'a' && t[0][0] == 'A');
        Vec<std::string> u = std::move(t);
        assert(t.size() == 0 && u.size() == 1);
        u = s;
        assert(u[0] == s[0]);
    }
    {
        Vec<Tracked> v;
        for (int i = 0; i < 1025; i++) v.push_back(Tracked(i));
        // each push: one move into the parameter is elided, one move into place;
        // each regrowth moves every element (noexcept): 1 + 2 + ... + 1024 = 2047
        assert(copies == 0 && moves == 1025 + 2047);
        Vec<Tracked> w = v;
        assert(copies == 1025);
        assert(alive == 2050);
    }
    assert(alive == 0);                           // every element destroyed exactly once
    {
        Vec<std::unique_ptr<int>> p;              // a move-only type works too
        for (int i = 0; i < 10; i++) p.push_back(std::make_unique<int>(i));
        assert(*p[9] == 9);
    }
    {
        Vec<Fragile> f;
        for (int i = 0; i < 8; i++) f.push_back(Fragile(i));   // full: capacity 8
        Fragile::budget = 3;                                   // the 4th copy of the regrowth throws
        bool threw = false;
        try { f.push_back(Fragile(8)); } catch (const std::runtime_error &) { threw = true; }
        assert(threw && f.size() == 8 && f.capacity() == 8);  // strong: as before the call
        for (int i = 0; i < 8; i++) assert(f[std::size_t(i)].v == i);
    }
    std::puts("vec_test: OK");
    return 0;
}

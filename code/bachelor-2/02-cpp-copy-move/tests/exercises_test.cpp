// exercises_test.cpp: the solutions of exercises 7, 9, 10 and 12.
#include <cassert>
#include <cstdio>
#include <cstring>
#include <string>
#include <utility>
#include <vector>
#include "../exercises/observers_fixed.hpp"
#include "../exercises/small_string.hpp"
#include "../exercises/tree.hpp"
#include "../exercises/unique_ptr.hpp"

static int live = 0;
struct Probe {
    int v;
    explicit Probe(int x) : v(x) { live++; }
    ~Probe() { live--; }
};

static void test_unique()
{
    {
        UniquePtr<Probe> p(new Probe(7));
        assert(live == 1 && p && p->v == 7 && (*p).v == 7);
        UniquePtr<Probe> q = std::move(p);
        assert(!p && q && live == 1);
        UniquePtr<Probe> r(new Probe(8));
        r = std::move(q);                       // the old Probe(8) is freed
        assert(live == 1 && r->v == 7 && !q);
        r = std::move(r);                       // self-move keeps the object
        assert(live == 1 && r && r->v == 7);
        Probe *raw = r.release();
        assert(!r && live == 1);
        r.reset(raw);
        r.reset();
        assert(live == 0 && !r);
        std::vector<UniquePtr<Probe>> v;
        for (int i = 0; i < 100; i++)
            v.push_back(UniquePtr<Probe>(new Probe(i)));   // moved through regrowths
        assert(live == 100 && v[99]->v == 99);
    }
    assert(live == 0);
}

static void test_tree()
{
    Node root("town");
    Node &west = root.add("west");
    Node &east = root.add("east");
    Node &mill = west.add("mill");
    mill.add("wheel");
    assert(mill.children[0]->path() == "town/west/mill/wheel");
    west.move_child(0, east);                   // mill and wheel move to east
    assert(west.children.empty() && east.children.size() == 1);
    assert(east.children[0]->children[0]->path() == "town/east/mill/wheel");
    assert(&mill == east.children[0].get());    // the node itself did not move in memory
}

static void test_small()
{
    SmallString a("pier");
    SmallString b("a name of more than fifteen characters");
    assert(a.is_small() && !b.is_small());
    SmallString c = a, d = b;
    assert(std::strcmp(c.c_str(), "pier") == 0 && c.is_small());
    assert(std::strcmp(d.c_str(), b.c_str()) == 0 && d.c_str() != b.c_str());
    const char *block = d.c_str();
    SmallString e = std::move(d);
    assert(e.c_str() == block && d.size() == 0 && d.is_small() && std::strcmp(d.c_str(), "") == 0);
    SmallString f = std::move(c);
    assert(f.is_small() && std::strcmp(f.c_str(), "pier") == 0 && c.size() == 0);
    f = e;
    assert(!f.is_small() && std::strcmp(f.c_str(), b.c_str()) == 0);
    e = a;
    assert(e.is_small() && std::strcmp(e.c_str(), "pier") == 0);
    SmallString &self = e;
    e = self;
    e = std::move(self);
    assert(std::strcmp(e.c_str(), "pier") == 0);
    std::vector<SmallString> v;
    for (int i = 0; i < 50; i++)
        v.push_back(i % 2 ? SmallString("short") : SmallString("a rather long street name, number"));
    assert(std::strcmp(v[48].c_str(), "a rather long street name, number") == 0 && v[49].is_small());
}

static void test_observers()
{
    {
        auto s = std::make_shared<Station>();
        s->name = "Riverside";
        watch(s, "hall");
        watch(s, "office");
        assert(alive == 3 && s.use_count() == 1);
        auto d = s->watchers[0];
        assert(d->source.lock() == s);
    }
    assert(alive == 0);                         // every node freed
}

int main()
{
    test_unique();
    test_tree();
    test_small();
    test_observers();
    std::puts("exercises_test: OK");
    return 0;
}

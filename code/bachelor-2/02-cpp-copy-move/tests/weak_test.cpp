// weak_test.cpp: the cycle leaks two objects; with a weak edge every node is destroyed.
#include <cassert>
#include <cstdio>
#include <memory>

static int alive = 0;

struct B;
struct A {
    std::shared_ptr<B> b;
    A() { alive++; }
    ~A() { alive--; }
};
struct B {
    std::shared_ptr<A> strong;
    std::weak_ptr<A> weak;
    B() { alive++; }
    ~B() { alive--; }
};

int main()
{
    {
        auto a = std::make_shared<A>();
        a->b = std::make_shared<B>();
        a->b->weak = a;
        assert(a.use_count() == 1);
        assert(!a->b->weak.expired());
    }
    assert(alive == 0);                       // the weak edge: both freed
    std::weak_ptr<A> watcher;
    {
        auto a = std::make_shared<A>();
        a->b = std::make_shared<B>();
        a->b->strong = a;
        watcher = a;
        assert(a.use_count() == 2);
    }
    assert(alive == 2 && !watcher.expired()); // the strong cycle: both still alive
    watcher.lock()->b->strong.reset();        // break the cycle by hand
    assert(alive == 0 && watcher.expired());
    std::puts("weak_test: OK");
    return 0;
}

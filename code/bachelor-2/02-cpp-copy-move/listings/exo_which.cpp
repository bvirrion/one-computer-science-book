// exo_which.cpp (exercise 5): which special member runs?
#include <cstdio>
#include <utility>

struct W {
    W() { std::puts("default"); }
    W(const W &) { std::puts("copy constructor"); }
    W(W &&) noexcept { std::puts("move constructor"); }
    W &operator=(const W &) { std::puts("copy assignment"); return *this; }
    W &operator=(W &&) noexcept { std::puts("move assignment"); return *this; }
};

W make() { return W(); }
W named() { W w; return w; }

int main()
{
    W a;                         // 1
    W b(a);                      // 2
    W c = std::move(b);          // 3
    a = c;                       // 4
    a = make();                  // 5
    [[maybe_unused]] W d = make();   // 6
    [[maybe_unused]] W e = named();  // 7
    const W f;
    [[maybe_unused]] W g = std::move(f);   // 8
    return 0;
}

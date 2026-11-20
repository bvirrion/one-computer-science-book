// dispatch_cost.cpp: a direct call, a virtual call and a switch, timed per call.
#include <chrono>
#include <cstdio>
#include <memory>
#include <random>
#include <vector>

struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };
struct Sq : Shape { double s; explicit Sq(double x) : s(x) {} double area() const override { return s * s; } };
struct Ci : Shape { double r; explicit Ci(double x) : r(x) {} double area() const override { return 3.14159 * r * r; } };
struct Tagged { int kind; double x; };          // the C way: a tag and a switch

__attribute__((noinline)) double area_sq(const Sq &q) { return q.s * q.s; }
double area_tagged(const Tagged &t)
{
    switch (t.kind) {
    case 0: return t.x * t.x;
    default: return 3.14159 * t.x * t.x;
    }
}

template <class F> double ns_per(F f, int n)
{
    auto t0 = std::chrono::steady_clock::now();
    double sink = f();
    auto t1 = std::chrono::steady_clock::now();
    if (sink == 42.0) std::puts("");            // keep the result alive
    return std::chrono::duration<double, std::nano>(t1 - t0).count() / n;
}

int main()
{
    const int n = 10000000;
    std::mt19937 gen(7);
    std::vector<int> kinds(n);
    for (int &k : kinds) k = int(gen() % 2);    // a random mix of the two kinds
    std::vector<Sq> squares;
    std::vector<std::unique_ptr<Shape>> shapes, same;   // mixed kinds; squares only
    std::vector<Tagged> tagged;
    for (int i = 0; i < n; i++) {
        double x = 1.0 + i % 7;
        squares.emplace_back(x);
        same.push_back(std::make_unique<Sq>(x));
        if (kinds[i]) shapes.push_back(std::make_unique<Ci>(x)); else shapes.push_back(std::make_unique<Sq>(x));
        tagged.push_back({kinds[i], x});
    }
    double d = ns_per([&] { double s = 0; for (const auto &q : squares) s += area_sq(q); return s; }, n);
    double u = ns_per([&] { double s = 0; for (const auto &p : same) s += p->area(); return s; }, n);
    double v = ns_per([&] { double s = 0; for (const auto &p : shapes) s += p->area(); return s; }, n);
    double w = ns_per([&] { double s = 0; for (const auto &t : tagged) s += area_tagged(t); return s; }, n);
    std::printf("direct call (not inlined)  %5.2f ns\n", d);
    std::printf("virtual call, one kind     %5.2f ns\n", u);
    std::printf("virtual call, mixed kinds  %5.2f ns\n", v);
    std::printf("switch on a tag, inlined   %5.2f ns\n", w);
    return 0;
}

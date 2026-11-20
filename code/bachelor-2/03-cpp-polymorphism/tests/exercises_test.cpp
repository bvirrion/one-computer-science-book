// exercises_test.cpp: expression trees (exercise 10) and double dispatch (exercise 12).
#include <cassert>
#include <cstdio>
#include <memory>
#include <vector>
#include "../exercises/collide.hpp"
#include "../exercises/expr.hpp"

static ExprPtr num(double v) { return std::make_unique<Num>(v); }
static ExprPtr var(const char *n) { return std::make_unique<Var>(n); }
static ExprPtr add(ExprPtr a, ExprPtr b) { return std::make_unique<Add>(std::move(a), std::move(b)); }
static ExprPtr mul(ExprPtr a, ExprPtr b) { return std::make_unique<Mul>(std::move(a), std::move(b)); }

int main()
{
    // (x * (2 + 3)) + (0 * y)  simplifies to  (x * 5)
    ExprPtr e = add(mul(var("x"), add(num(2), num(3))), mul(num(0), var("y")));
    assert(e->str() == "((x * (2 + 3)) + (0 * y))");
    std::map<std::string, double> env{{"x", 1.5}, {"y", 7}};
    assert(e->eval(env) == 7.5);
    ExprPtr s = e->simplify();
    assert(s->str() == "(x * 5)");
    assert(s->eval(env) == 7.5);
    assert(mul(num(1), add(var("y"), num(0)))->simplify()->str() == "y");
    assert(add(num(2.5), num(0.25))->simplify()->str() == "2.75");
    bool threw = false;
    try { var("z")->eval(env); } catch (const std::out_of_range &) { threw = true; }
    assert(threw);

    std::vector<std::unique_ptr<Body>> b;
    b.push_back(std::make_unique<Disc>(0, 0, 1));
    b.push_back(std::make_unique<Box>(1.5, -1, 3, 1));          // 0.5 to the right of the disc
    b.push_back(std::make_unique<Disc>(2, 0, 0.6));             // inside the first box, clear of the disc
    b.push_back(std::make_unique<Box>(0.5, 0.5, 2, 2));         // corner inside the disc's square
    bool expect[4][4] = {{1, 0, 0, 1}, {0, 1, 1, 1}, {0, 1, 1, 1}, {1, 1, 1, 1}};
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            assert(b[std::size_t(i)]->hits(*b[std::size_t(j)]) == expect[i][j]);
    std::puts("exercises_test: OK");
    return 0;
}

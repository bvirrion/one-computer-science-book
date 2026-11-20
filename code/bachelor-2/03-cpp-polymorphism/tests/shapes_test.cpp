// shapes_test.cpp: dispatch on the shapes of the text and the Triangle of exercise 3.
#include <cassert>
#include <cmath>
#include <cstring>
#include <memory>
#include <stdexcept>
#include <vector>
#include "shapes.hpp"
#include "../exercises/triangle.hpp"

int main()
{
    std::vector<std::unique_ptr<Shape>> v;
    v.push_back(std::make_unique<Rectangle>(12.0, 8.5));
    v.push_back(std::make_unique<Circle>(1.0));
    v.push_back(std::make_unique<Triangle>(3.0, 4.0, 5.0));
    assert(v[0]->area() == 102.0);
    assert(std::fabs(v[1]->area() - 3.14159265358979) < 1e-12);
    assert(std::fabs(v[2]->area() - 6.0) < 1e-12);
    assert(std::strcmp(v[2]->name(), "triangle") == 0);
    const Shape &ref = *v[1];
    assert(std::strcmp(ref.name(), "circle") == 0);
    bool threw = false;
    try { Triangle t(1, 2, 3); } catch (const std::invalid_argument &) { threw = true; }
    assert(threw);                                  // a flat triangle is refused
    std::puts("shapes_test: OK");
    return 0;
}

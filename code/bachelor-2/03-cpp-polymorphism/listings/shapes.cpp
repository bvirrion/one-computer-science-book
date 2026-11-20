// shapes.cpp: calls dispatched at run time to the class of each object.
#include <memory>
#include <vector>
#include "shapes.hpp"

int main()
{
    std::vector<std::unique_ptr<Shape>> plan;        // the plot plan of a garden
    plan.push_back(std::make_unique<Rectangle>(12.0, 8.5));
    plan.push_back(std::make_unique<Circle>(2.5));
    plan.push_back(std::make_unique<Rectangle>(3.0, 3.0));
    double total = 0;
    for (const auto &s : plan) {
        s->describe();                               // area() and name() of the real class
        total += s->area();
    }
    std::printf("total     area %8.2f\n", total);
    return 0;
}

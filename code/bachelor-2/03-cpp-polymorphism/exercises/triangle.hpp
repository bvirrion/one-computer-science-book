// triangle.hpp (exercise 3): a new kind of shape in a new file; no other file changes.
#pragma once
#include <cmath>
#include <stdexcept>
#include "shapes.hpp"

class Triangle : public Shape {
public:
    Triangle(double a, double b, double c) : a_(a), b_(b), c_(c)
    {
        if (a <= 0 || b <= 0 || c <= 0 || a + b <= c || a + c <= b || b + c <= a)
            throw std::invalid_argument("not a triangle");
    }
    double area() const override                    // Heron's formula
    {
        double s = (a_ + b_ + c_) / 2;
        return std::sqrt(s * (s - a_) * (s - b_) * (s - c_));
    }
    const char *name() const override { return "triangle"; }

private:
    double a_, b_, c_;
};

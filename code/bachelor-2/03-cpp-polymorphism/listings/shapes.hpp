// shapes.hpp: one base class and two derived classes.
#pragma once
#include <cstdio>

class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;                 // every shape has one; no default
    virtual const char *name() const { return "shape"; }
    void describe() const { std::printf("%-9s area %8.2f\n", name(), area()); }
};

class Circle : public Shape {
public:
    explicit Circle(double r) : r_(r) {}
    double area() const override { return 3.14159265358979 * r_ * r_; }
    const char *name() const override { return "circle"; }

private:
    double r_;
};

class Rectangle : public Shape {
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
    const char *name() const override { return "rectangle"; }

protected:                                         // visible to classes derived from Rectangle
    double w_, h_;
};

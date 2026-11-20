// collide.hpp (exercise 12): intersection tests chosen by the classes of both shapes.
#pragma once
#include <algorithm>
#include <cmath>

struct Disc;
struct Box;

struct Body {
    virtual ~Body() = default;
    virtual bool hits(const Body &other) const = 0;  // first dispatch: on *this
    virtual bool hits_disc(const Disc &d) const = 0; // second dispatch: on other
    virtual bool hits_box(const Box &b) const = 0;
};

struct Disc : Body {
    double x, y, r;
    Disc(double x_, double y_, double r_) : x(x_), y(y_), r(r_) {}
    bool hits(const Body &o) const override { return o.hits_disc(*this); }
    bool hits_disc(const Disc &d) const override
    {
        return std::hypot(x - d.x, y - d.y) <= r + d.r;
    }
    bool hits_box(const Box &b) const override;
};

struct Box : Body {                                   // sides parallel to the axes
    double x0, y0, x1, y1;
    Box(double a, double b, double c, double d) : x0(a), y0(b), x1(c), y1(d) {}
    bool hits(const Body &o) const override { return o.hits_box(*this); }
    bool hits_disc(const Disc &d) const override     // the point of the box nearest the centre
    {
        double nx = std::clamp(d.x, x0, x1), ny = std::clamp(d.y, y0, y1);
        return std::hypot(d.x - nx, d.y - ny) <= d.r;
    }
    bool hits_box(const Box &b) const override
    {
        return x0 <= b.x1 && b.x0 <= x1 && y0 <= b.y1 && b.y0 <= y1;
    }
};

inline bool Disc::hits_box(const Box &b) const { return b.hits_disc(*this); }   // symmetric

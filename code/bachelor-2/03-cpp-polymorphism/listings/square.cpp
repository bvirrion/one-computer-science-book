// square.cpp: a Square that is a Rectangle breaks a client of Rectangle.
#include <cstdio>

class Rectangle {
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    virtual ~Rectangle() = default;
    virtual void set_width(double w) { w_ = w; }    // postcondition: width w, height unchanged
    virtual void set_height(double h) { h_ = h; }   // postcondition: height h, width unchanged
    double area() const { return w_ * h_; }

protected:
    double w_, h_;
};

class Square : public Rectangle {                    // keeps its sides equal
public:
    explicit Square(double s) : Rectangle(s, s) {}
    void set_width(double w) override { w_ = h_ = w; }
    void set_height(double h) override { w_ = h_ = h; }
};

// A client written against Rectangle: resize a plot to 4 m by 5 m.
bool resize_plot(Rectangle &r)
{
    r.set_width(4);
    r.set_height(5);
    return r.area() == 20;                           // what the postconditions promise
}

int main()
{
    Rectangle r(2, 3);
    Square s(3);
    bool ok_r = resize_plot(r), ok_s = resize_plot(s);
    std::printf("rectangle: %s (area %g)\n", ok_r ? "as promised" : "broken", r.area());
    std::printf("square:    %s (area %g)\n", ok_s ? "as promised" : "broken", s.area());
    return 0;
}

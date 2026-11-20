// exo_captures.cpp: predict the four lines.
#include <cstdio>

int main()
{
    int fine = 10;
    auto by_value = [fine] { return fine; };
    auto by_ref = [&fine] { return fine; };
    auto counter = [n = 0]() mutable { return ++n; };   // its own variable, kept between calls
    fine = 25;
    std::printf("%d %d\n", by_value(), by_ref());
    auto copy = counter;
    counter();
    counter();
    std::printf("%d %d\n", counter(), copy());
    auto all = [=] { return fine * 2; };
    auto all_ref = [&] { return fine * 2; };
    fine = 0;
    std::printf("%d %d\n", all(), all_ref());
    std::printf("%zu %zu\n", sizeof by_value, sizeof all_ref);
    return 0;
}

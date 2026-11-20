// rule_of_zero.cpp: a class whose members manage themselves needs no special members.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

struct Station {                        // rule of zero: none of the five is written
    std::string name;
    std::vector<double> readings;
};

struct Sensor {                         // a move-only member makes the class move-only
    std::string id;
    std::unique_ptr<int> calibration;
};

int main()
{
    Station a{"Riverside", {18.5, 19.0}};
    Station b = a;                      // member-wise copy: a deep copy
    b.readings.push_back(21.5);
    Station c = std::move(b);           // member-wise move
    std::cout << a.readings.size() << ' ' << c.readings.size() << ' '
              << b.readings.size() << '\n';
    Sensor s{"T-4", std::make_unique<int>(12)};
    Sensor t = std::move(s);            // fine; Sensor u = t; would not compile
    std::cout << t.id << ' ' << *t.calibration << ' '
        << (s.calibration ? "full" : "empty") << '\n';
    return 0;
}

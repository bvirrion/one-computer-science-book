// vec_demo.cpp: one class template, three classes.
#include <iostream>
#include <string>
#include "vec.hpp"

int main()
{
    Vec<int> squares;
    Vec<double> quarters;
    Vec<std::string> streets;
    for (int i = 1; i <= 5; i++) {
        squares.push_back(i * i);
        quarters.push_back(i / 4.0);
    }
    streets.push_back("Mill Lane");
    streets.push_back("Quay Street");
    Vec<std::string> copy = streets;            // the template's copy constructor, for strings
    copy[0] = "Harbour Road";
    for (int x : squares) std::cout << x << ' ';
    std::cout << "| " << quarters[4] << " | " << streets[0] << ", " << copy[0] << '\n';
    std::cout << "sizes " << sizeof(Vec<int>) << ' '
        << sizeof(Vec<std::string>) << " bytes, capacity "
              << squares.capacity() << '\n';
    return 0;
}

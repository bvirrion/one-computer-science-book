// exo_dangling.cpp: the longer of two names, returned by reference.
#include <iostream>
#include <string>
// capture: exit
const std::string &longer(const std::string &a, const std::string &b)
{
    std::string result = a.size() >= b.size() ? a : b;
    return result;
}

int main()
{
    std::string x = "Harbour Road", y = "Elm Row";
    std::cout << longer(x, y) << '\n';
    return 0;
}

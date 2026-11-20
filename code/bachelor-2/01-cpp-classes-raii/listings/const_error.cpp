// const_error.cpp: a const reference cannot be written through (staged error).
#include <iostream>
// capture: exit
void add_bonus(const int &score)
{
    score += 10;                     // the compiler refuses
    std::cout << score << '\n';
}

int main()
{
    int s = 75;
    add_bonus(s);
    return 0;
}

// no_virtual_dtor.cpp: deleting a derived object through a base pointer without a virtual destructor.
// capture: cflags=-O0 -g -fsanitize=address exit
#include <cstdio>
#include <string>

struct Item {
    ~Item() { std::puts("~Item"); }              // not virtual
    int id = 0;
};

struct Recording : Item {
    ~Recording() { std::puts("~Recording"); }
    std::string tracks[4] = {"intro", "harbour", "tide", "coda"};
};

int main()
{
    std::setvbuf(stdout, nullptr, _IONBF, 0);   // unbuffered: the report ends the program
    Item *it = new Recording;
    delete it;                                   // undefined behaviour
    return 0;
}

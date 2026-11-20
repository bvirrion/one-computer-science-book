// ctor_order.cpp: bases are built first and destroyed last.
#include <cstdio>
#include <string>

struct Part {
    std::string s;
    explicit Part(std::string x) : s(std::move(x))
        { std::printf("  make member %s\n", s.c_str()); }
    ~Part() { std::printf("  drop member %s\n", s.c_str()); }
};

struct Item {
    Part code{"code"};
    Item() { std::printf("  Item body\n"); }
    ~Item() { std::printf("  ~Item body\n"); }
};

struct Map : Item {                      // a Map is an Item, with one more member
    Part sheet{"sheet"};
    Map() { std::printf("  Map body\n"); }
    ~Map() { std::printf("  ~Map body\n"); }
};

int main()
{
    std::puts("make a Map:");
    {
        Map m;
        std::puts("drop it:");
    }
    return 0;
}

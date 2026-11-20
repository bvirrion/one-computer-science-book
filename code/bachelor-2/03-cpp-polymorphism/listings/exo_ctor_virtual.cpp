// exo_ctor_virtual.cpp (exercise 5): a virtual call made by a constructor.
#include <cstdio>
#include <string>

struct Item {
    Item() { std::printf("Item(): %s\n", describe().c_str()); }
    virtual ~Item() { std::printf("~Item(): %s\n", describe().c_str()); }
    virtual std::string describe() const { return "an item"; }
    void show() const { std::printf("show(): %s\n", describe().c_str()); }
};
struct Map : Item {
    std::string region = "the coast";
    Map() { std::printf("Map(): %s\n", describe().c_str()); }
    std::string describe() const override { return "a map of " + region; }
};

int main()
{
    Map m;
    m.show();
    return 0;
}

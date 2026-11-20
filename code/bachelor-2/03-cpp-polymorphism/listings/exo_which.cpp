// exo_which.cpp (exercise 1): which function runs?
#include <cstdio>

struct Item {
    virtual ~Item() = default;
    virtual const char *kind() const { return "item"; }
    const char *shelf() const { return "general shelf"; }      // not virtual
};
struct Map : Item {
    const char *kind() const override { return "map"; }
    const char *shelf() const { return "map drawer"; }          // hides Item::shelf
};

void through_pointer(const Item *p)
    { std::printf("pointer:   %s, %s\n", p->kind(), p->shelf()); }
void through_ref(const Item &r) { std::printf("reference: %s, %s\n", r.kind(), r.shelf()); }
void through_value(Item v) { std::printf("value:     %s, %s\n", v.kind(), v.shelf()); }

int main()
{
    Map m;
    through_pointer(&m);
    through_ref(m);
    through_value(m);
    std::printf("direct:    %s, %s\n", m.kind(), m.shelf());
    return 0;
}

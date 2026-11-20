// sizes.cpp: one table pointer per object, whatever the number of virtual functions.
#include <cstdio>

struct Plain { int id; };
struct OneVirtual { virtual ~OneVirtual() = default; int id; };
struct ManyVirtual {
    virtual ~ManyVirtual() = default;
    virtual void a() {}
    virtual void b() {}
    virtual void c() {}
    int id;
};
struct Derived : ManyVirtual { void a() override {} int extra; };

int main()
{
    std::printf("pointer      %2zu bytes\n", sizeof(void *));
    std::printf("Plain        %2zu bytes\n", sizeof(Plain));
    std::printf("OneVirtual   %2zu bytes\n", sizeof(OneVirtual));
    std::printf("ManyVirtual  %2zu bytes\n", sizeof(ManyVirtual));
    std::printf("Derived      %2zu bytes\n", sizeof(Derived));
    ManyVirtual x, y;
    Derived d;
    // the table pointer is the first 8 bytes of each object (an implementation detail)
    auto table = [](const void *obj) { return *static_cast<void *const *>(obj); };
    std::printf("x and y share a table: %s; d has another: %s\n",
                table(&x) == table(&y) ? "yes" : "no", table(&x) != table(&d) ? "yes" : "no");
    return 0;
}

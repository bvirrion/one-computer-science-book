// exo_slice_vector.cpp (exercise 6): a catalogue of items kept in a vector.
#include <cstdio>
#include <string>
#include <vector>

struct Item {
    std::string title;
    virtual ~Item() = default;
    virtual std::string label() const { return title; }
};
struct Recording : Item {
    int minutes = 0;
    std::string label() const override
        { return title + " (" + std::to_string(minutes) + " min)"; }
};

int main()
{
    std::vector<Item> catalogue;
    Recording r;
    r.title = "Harbour Songs";
    r.minutes = 42;
    catalogue.push_back(r);
    Item book;
    book.title = "The Silent Code";
    catalogue.push_back(book);
    for (const Item &it : catalogue)
        std::printf("%s\n", it.label().c_str());
    return 0;
}

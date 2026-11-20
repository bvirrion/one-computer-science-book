// slicing.cpp: a derived object copied into a base object loses its derived part.
#include <cstdio>
#include <string>

class Item {
public:
    explicit Item(std::string t) : title_(std::move(t)) {}
    virtual ~Item() = default;
    virtual std::string label() const { return title_; }

protected:
    std::string title_;
};

class Recording : public Item {
public:
    Recording(std::string t, int minutes) : Item(std::move(t)), minutes_(minutes) {}
    std::string label() const override
        { return title_ + " (" + std::to_string(minutes_) + " min)"; }

private:
    int minutes_;
};

void by_value(Item it) { std::printf("by value:     %s\n", it.label().c_str()); }
void by_reference(const Item &it) { std::printf("by reference: %s\n", it.label().c_str()); }

int main()
{
    Recording r("Harbour Songs", 42);
    by_reference(r);
    by_value(r);                      // the parameter is an Item built from the Item part of r
    Item copy = r;                     // the same slicing
    std::printf("copy:         %s\n", copy.label().c_str());
    std::printf("sizeof(Item) = %zu, sizeof(Recording) = %zu\n",
        sizeof(Item), sizeof(Recording));
    return 0;
}

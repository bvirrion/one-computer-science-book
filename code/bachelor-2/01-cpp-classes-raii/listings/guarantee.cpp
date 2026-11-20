// guarantee.cpp: two ways to add several names; only one keeps the strong guarantee.
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

class Roster {
public:
    // Basic guarantee: on failure the roster is valid, but may hold some new names.
    void add_all_basic(const std::vector<std::string> &names)
    {
        for (const std::string &n : names)
            names_.push_back(checked(n));
    }
    // Strong guarantee: on failure the roster is exactly as before.
    void add_all_strong(const std::vector<std::string> &names)
    {
        std::vector<std::string> copy = names_;
        for (const std::string &n : names)
            copy.push_back(checked(n));
        names_.swap(copy);           // cannot throw
    }
    std::size_t size() const { return names_.size(); }

private:
    static const std::string &checked(const std::string &n)
    {
        if (n.empty())
            throw std::invalid_argument("empty name");
        return n;
    }
    std::vector<std::string> names_{"Ada", "Brendan"};
};

int main()
{
    const std::vector<std::string> batch{"Cora", "Dev", "", "Emil"};
    Roster a, b;
    try { a.add_all_basic(batch); } catch (const std::invalid_argument &e) {
        std::cout << "basic:  " << e.what() << ", size now " << a.size() << '\n';
    }
    try { b.add_all_strong(batch); } catch (const std::invalid_argument &e) {
        std::cout << "strong: " << e.what() << ", size now " << b.size() << '\n';
    }
    return 0;
}

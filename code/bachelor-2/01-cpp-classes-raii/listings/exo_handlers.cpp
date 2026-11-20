// exo_handlers.cpp: which handler catches each throw?
#include <iostream>
#include <stdexcept>

void step(int k)
{
    try {
        if (k == 1) throw std::invalid_argument("one");
        if (k == 2) throw std::out_of_range("two");
        if (k == 3) throw std::runtime_error("three");
        if (k == 4) throw 4;
    } catch (const std::out_of_range &e) {
        std::cout << k << ": inner out_of_range " << e.what() << '\n';
    } catch (const std::invalid_argument &e) {
        std::cout << k << ": inner invalid_argument " << e.what() << '\n';
        throw;
    }
    std::cout << k << ": step done\n";
}

int main()
{
    for (int k = 0; k <= 4; k++) {
        try {
            try {
                step(k);
            } catch (const std::logic_error &e) {
                std::cout << k << ": middle logic_error " << e.what() << '\n';
            }
        } catch (const std::exception &e) {
            std::cout << k << ": outer exception " << e.what() << '\n';
        } catch (...) {
            std::cout << k << ": outer catch-all\n";
        }
    }
    return 0;
}

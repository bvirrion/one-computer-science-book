// exo_two_files.cpp: a constructor that opens two files and may fail half way.
#include <cstdio>
#include <fcntl.h>
#include <iostream>
#include <stdexcept>

class Merger {
public:
    Merger(const char *first, const char *second)
        : a_(std::fopen(first, "r")), b_(std::fopen(second, "r"))
    {
        if (a_ == nullptr || b_ == nullptr)
            throw std::runtime_error("cannot open both files");
    }
    ~Merger()
    {
        std::fclose(a_);
        std::fclose(b_);
    }

private:
    std::FILE *a_;
    std::FILE *b_;
};

int open_files()
{
    int n = 0;
    for (int fd = 0; fd < 256; fd++)
        n += fcntl(fd, F_GETFD) != -1;
    return n;
}

int main()
{
    for (int i = 0; i < 5; i++) {
        try {
            Merger m("good.log", "missing.log");
        } catch (const std::runtime_error &e) {
            std::cout << e.what() << "; open files: " << open_files() << '\n';
        }
    }
    return 0;
}

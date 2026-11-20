// shallow.cpp: the copy the compiler writes copies the pointer, not the block.
// capture: cflags=-O0 -g -fsanitize=address exit
#include <cstring>
#include <iostream>

class Buffer {
public:
    explicit Buffer(const char *text) : n_(std::strlen(text)), data_(new char[n_ + 1])
    {
        std::memcpy(data_, text, n_ + 1);
    }
    ~Buffer() { delete[] data_; }
    const char *c_str() const { return data_; }

private:
    std::size_t n_;
    char *data_;
};

int main()
{
    Buffer a("Harbour Road");
    Buffer b = a;                    // the implicit copy constructor
    std::cout << a.c_str() << " / " << b.c_str() << '\n';
    return 0;                        // b is destroyed, then a: the same block twice
}

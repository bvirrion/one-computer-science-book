// move_demo.cpp: a Buffer that can be moved as well as copied.
// capture: cflags=-O0 -g -fsanitize=address
#include <cstdio>
#include <cstring>
#include <utility>

class Buffer {
public:
    explicit Buffer(const char *t) : n_(std::strlen(t)), data_(new char[n_ + 1])
    {
        std::memcpy(data_, t, n_ + 1);
    }
    ~Buffer() { delete[] data_; }
    Buffer(const Buffer &o) : n_(o.n_), data_(new char[n_ + 1])
    {
        std::memcpy(data_, o.data_, n_ + 1);
        std::puts("  copy constructor");
    }
    Buffer(Buffer &&o) noexcept : n_(o.n_), data_(o.data_)     // steal the block
    {
        o.n_ = 0;
        o.data_ = nullptr;                                     // the source owns nothing
        std::puts("  move constructor");
    }
    const char *c_str() const { return data_ ? data_ : "(empty)"; }

private:
    std::size_t n_;
    char *data_;
};

Buffer label(const char *t) { return Buffer(t); }   // a prvalue: built in place

int main()
{
    Buffer a("Mill Lane");
    std::puts("Buffer b = a;");
    Buffer b = a;                       // a is an lvalue: copy
    std::puts("Buffer c = std::move(a);");
    Buffer c = std::move(a);            // std::move(a) is an xvalue: move
    std::puts("Buffer d = label(...);");
    Buffer d = label("Quay Street");    // guaranteed elision: neither
    std::printf("a=%s b=%s c=%s d=%s\n", a.c_str(), b.c_str(), c.c_str(), d.c_str());
    return 0;
}

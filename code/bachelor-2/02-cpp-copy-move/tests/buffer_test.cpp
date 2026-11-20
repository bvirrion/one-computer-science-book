// buffer_test.cpp: the deep-copy Buffer of the text and the rule-of-five Buffer of exercise 3.
#include <cassert>
#include <cstdio>
#include <cstring>
#include <utility>
#include "buffer.hpp"
namespace five {
#include "../exercises/buffer5.hpp"
}

int main()
{
    {
        Buffer a("harbour");
        Buffer b = a;
        assert(a.c_str() != b.c_str() && std::strcmp(a.c_str(), b.c_str()) == 0);
        b.upcase_first();
        assert(std::strcmp(a.c_str(), "harbour") == 0 && std::strcmp(b.c_str(), "Harbour") == 0);
        Buffer c("x");
        c = a;
        assert(std::strcmp(c.c_str(), "harbour") == 0 && c.c_str() != a.c_str());
        Buffer &self = c;
        c = self;
        assert(std::strcmp(c.c_str(), "harbour") == 0);
    }
    {
        five::Buffer a("quay");
        five::Buffer b = a;
        assert(b.c_str() != a.c_str() && std::strcmp(b.c_str(), "quay") == 0);
        const char *block = a.c_str();
        five::Buffer c = std::move(a);
        assert(c.c_str() == block && a.size() == 0 && std::strcmp(a.c_str(), "") == 0);
        five::Buffer d("long name for a street");
        d = std::move(c);
        assert(d.c_str() == block && std::strcmp(d.c_str(), "quay") == 0);
        d = b;
        assert(std::strcmp(d.c_str(), "quay") == 0 && d.c_str() != b.c_str());
        five::Buffer &self = d;
        d = self;
        assert(std::strcmp(d.c_str(), "quay") == 0);
        a = five::Buffer("reused");               // a moved-from object can be assigned again
        assert(std::strcmp(a.c_str(), "reused") == 0);
    }
    std::puts("buffer_test: OK");
    return 0;
}

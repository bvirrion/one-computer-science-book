// file_handle_test.cpp: File closes its FILE on every path, including throws.
#include <cassert>
#include <cstdio>
#include <stdexcept>
#include <string>
#include "file_handle.hpp"
#include "open_files.hpp"

static int first_line_length(const std::string &path, bool throw_after_open)
{
    File f(path, "r");
    if (throw_after_open)
        throw std::logic_error("thrown with the file open");
    auto line = f.read_line();
    return line ? static_cast<int>(line->size()) : -1;
}

int main()
{
    const int base = count_open_files();
    assert(first_line_length("../listings/good.log", false) == 27);
    assert(count_open_files() == base);
    for (int i = 0; i < 20; i++) {
        try { first_line_length("../listings/good.log", true); assert(false); }
        catch (const std::logic_error &) {}
    }
    assert(count_open_files() == base);
    bool refused = false;
    try { File f("../listings/missing.log", "r"); } catch (const std::runtime_error &) { refused = true; }
    assert(refused && count_open_files() == base);
    {
        File f("../listings/good.log", "r");
        assert(f.read_line() == std::string("LOG v2 town weather station"));
        assert(f.read_line() == std::string("2025-06-14 riverside 18.5"));
        assert(!f.read_line());
        assert(count_open_files() == base + 1);
    }
    bool full = false;
    try { File f("/dev/full", "a"); f.write("x\n"); f.flush(); } catch (const std::runtime_error &) { full = true; }
    assert(full && count_open_files() == base);
    std::puts("file_handle_test: ok");
    return 0;
}

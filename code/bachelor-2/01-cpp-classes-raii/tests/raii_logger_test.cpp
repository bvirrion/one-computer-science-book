// raii_logger_test.cpp: append_readings writes the batch whole, or throws and leaks nothing.
#include <cassert>
#include <cstdio>
#include <stdexcept>
#include <string>
#define main raii_logger_main
#include "../listings/raii_logger.cpp"
#undef main
#include "open_files.hpp"

static std::string slurp(const char *path)
{
    std::string s;
    std::FILE *f = std::fopen(path, "r");
    for (int c; (c = std::fgetc(f)) != EOF;)
        s += static_cast<char>(c);
    std::fclose(f);
    return s;
}

int main()
{
    const char *path = "raii_logger_test.tmp";
    std::remove(path);
    const int base = count_open_files();
    append_readings(path, {18.5, 19.25, 17.0});
    append_readings(path, {-3.0});
    assert(slurp(path) == "18.5\n19.2\n17.0\n-3.0\n");      // %.1f rounds 19.25 to even: 19.2
    bool refused = false;
    try { append_readings(path, {1.0, -99.0}); } catch (const std::invalid_argument &) { refused = true; }
    assert(refused && slurp(path) == "18.5\n19.2\n17.0\n-3.0\n");   // nothing half written
    for (int i = 0; i < 10; i++) {
        try { append_readings("/dev/full", {1.0}); assert(false); } catch (const std::runtime_error &) {}
    }
    assert(count_open_files() == base);
    std::remove(path);
    std::puts("raii_logger_test: ok");
    return 0;
}

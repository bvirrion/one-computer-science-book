// raii_logger.cpp: the same batch in C++; every resource is owned by an object.
#include <cstdio>
#include <fcntl.h>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "file_handle.hpp"

void append_readings(const std::string &path, const std::vector<double> &t)
{
    std::string buf;                     // owns its own memory
    for (double x : t) {
        if (x < -90.0)
            throw std::invalid_argument("error code in the data");
        char cell[16];
        std::snprintf(cell, sizeof cell, "%.1f\n", x);
        buf += cell;
    }
    File f(path, "a");                   // throws if it cannot open
    f.write(buf);
    f.flush();                           // throws if the disk is full
}

int open_files()
{
    int n = 0;
    for (int fd = 0; fd < 256; fd++)
        n += fcntl(fd, F_GETFD) != -1;
    return n;
}

int main()
{
    const std::vector<double> ok{18.5, 19.25, 17.0}, bad{18.5, -99.0, 17.0};
    const std::vector<std::pair<std::string, std::vector<double>>> runs{
        {"no_such_dir/w.log", ok}, {"/dev/null", bad}, {"/dev/null", ok}, {"/dev/full", ok}};
    for (const auto &[path, data] : runs) {
        std::string result = "ok";
        try {
            append_readings(path, data);
        } catch (const std::exception &e) {
            result = e.what();
        }
        std::printf("%-18s %-34s open files now %d\n", path.c_str(), result.c_str(), open_files());
    }
    return 0;
}

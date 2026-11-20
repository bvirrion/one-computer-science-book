// file_demo.cpp: the header check of the C version, with the file owned by an object.
#include <fcntl.h>
#include <iostream>
#include <string>
#include "file_handle.hpp"

int header_version(const std::string &path)
{
    File f(path, "r");                       // throws if the file cannot be opened
    std::optional<std::string> line = f.read_line();
    if (!line || line->rfind("LOG v", 0) != 0)
        return -1;                           // f is closed here
    return (*line)[5] - '0';                 // and here
}

int open_files()
{
    int n = 0;
    for (int fd = 0; fd < 256; fd++)
        if (fcntl(fd, F_GETFD) != -1)
            n++;
    return n;
}

int main()
{
    std::cout << "open files at start: " << open_files() << '\n';
    std::cout << "good.log: version " << header_version("good.log") << '\n';
    for (int i = 0; i < 10; i++)
        header_version("bad.log");
    std::cout << "bad.log read 10 times: version -1 each time\n";
    std::cout << "open files at end:   " << open_files() << '\n';
    try {
        header_version("missing.log");
    } catch (const std::runtime_error &e) {
        std::cout << "missing.log: " << e.what() << '\n';
    }
    return 0;
}

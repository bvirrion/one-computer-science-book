// open_files.hpp: test helper, the number of open descriptors 0..255.
#pragma once
#include <fcntl.h>

inline int count_open_files()
{
    int n = 0;
    for (int fd = 0; fd < 256; fd++)
        n += fcntl(fd, F_GETFD) != -1;
    return n;
}

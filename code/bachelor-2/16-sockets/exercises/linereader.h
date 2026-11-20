/* linereader.h: read a stream line by line, with a buffer of its own (exercise 7). */
#ifndef LINEREADER_H
#define LINEREADER_H

#include <stddef.h>
#include <sys/types.h>

struct linereader {
    int fd;
    size_t start, end;                           /* unread bytes: buf[start .. end) */
    char buf[4096];
};

void lr_init(struct linereader *r, int fd);
ssize_t lr_line(struct linereader *r, char *out, size_t cap);  /* length; -1 at end */

#endif

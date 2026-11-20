/* linereader.c: one recv may hold several lines, or part of one; keep the rest. */
#include <string.h>
#include <sys/socket.h>

#include "linereader.h"

void lr_init(struct linereader *r, int fd)
{
    r->fd = fd;
    r->start = r->end = 0;
}

ssize_t lr_line(struct linereader *r, char *out, size_t cap)
{
    for (;;) {
        char *nl = memchr(r->buf + r->start, '\n', r->end - r->start);
        if (nl) {                                /* a whole line is buffered */
            size_t n = nl - (r->buf + r->start);
            size_t k = n < cap - 1 ? n : cap - 1;    /* a longer line is cut */
            memcpy(out, r->buf + r->start, k);
            out[k] = '\0';
            r->start += n + 1;
            return k;
        }
        if (r->start > 0) {                      /* make room: move the rest down */
            memmove(r->buf, r->buf + r->start, r->end - r->start);
            r->end -= r->start;
            r->start = 0;
        }
        if (r->end == sizeof r->buf)
            r->end = 0;                          /* no newline in 4096 bytes: drop them */
        ssize_t k = recv(r->fd, r->buf + r->end, sizeof r->buf - r->end, 0);
        if (k <= 0)
            return -1;                           /* end (a last partial line is lost) */
        r->end += k;
    }
}

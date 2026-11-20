/* chat.c: one thread, poll, every line sent to every other client (exercise 10). */
#define _POSIX_C_SOURCE 200809L
#include <poll.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "../listings/net.h"

#define MAXC 32

struct client { int fd; size_t len; char buf[1024]; };

static void broadcast(struct client *cl, int n, int from, const char *line, size_t len)
{
    for (int i = 0; i < n; i++)
        if (i != from)
            send_all(cl[i].fd, line, len);       /* small lines: a full buffer would block */
}

void chat_serve(int lfd, int total)             /* until `total` clients came and left */
{
    struct client cl[MAXC];
    struct pollfd p[MAXC + 1];
    int n = 0, seen = 0;
    while (seen < total || n > 0) {
        p[0] = (struct pollfd){.fd = seen < total ? lfd : -1, .events = POLLIN};
        for (int i = 0; i < n; i++)
            p[i + 1] = (struct pollfd){.fd = cl[i].fd, .events = POLLIN};
        poll(p, n + 1, -1);
        for (int i = n - 1; i >= 0; i--) {
            if (!(p[i + 1].revents & (POLLIN | POLLHUP)))
                continue;
            struct client *c = &cl[i];
            ssize_t k = recv(c->fd, c->buf + c->len, sizeof c->buf - c->len, 0);
            if (k <= 0) {                        /* gone: close and forget */
                close(c->fd);
                cl[i] = cl[--n];
                continue;
            }
            c->len += k;
            char *nl;
            while ((nl = memchr(c->buf, '\n', c->len))) {   /* every complete line */
                size_t len = nl - c->buf + 1;
                broadcast(cl, n, i, c->buf, len);
                memmove(c->buf, c->buf + len, c->len - len);
                c->len -= len;
            }
            if (c->len == sizeof c->buf)
                c->len = 0;                      /* a line too long: dropped */
        }
        if ((p[0].revents & POLLIN) && n < MAXC) {
            cl[n] = (struct client){.fd = accept(lfd, NULL, NULL)};
            n++, seen++;
        }
    }
}

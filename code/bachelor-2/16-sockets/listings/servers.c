/* servers.c: a connection brings one framed request; the server answers and closes. */
#define _POSIX_C_SOURCE 200809L
#include <poll.h>
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

#include "directory.h"
#include "net.h"
#include "servers.h"

static void handle(int c)                        /* read one request, answer, close */
{
    char req[256], reply[256];
    ssize_t n = recv_msg(c, req, sizeof req);
    if (n >= 0)
        send_msg(c, reply, directory_answer(req, n, reply, sizeof reply));
    close(c);
}

void serve_fork(int lfd, long connections)
{
    for (long k = 0; k < connections; k++) {
        int c = accept(lfd, NULL, NULL);
        if (fork() == 0) {                       /* the child serves ... */
            close(lfd);
            handle(c);
            _exit(0);
        }
        close(c);                                /* ... the parent goes back to accept */
        while (waitpid(-1, NULL, WNOHANG) > 0)
            ;                                    /* reap the children that are done */
    }
    while (wait(NULL) > 0)
        ;
}

static atomic_long finished;                     /* threads done, for the end only */

static void *handle_thread(void *arg)
{
    handle((int)(intptr_t)arg);
    atomic_fetch_add(&finished, 1);
    return NULL;
}

void serve_threads(int lfd, long connections)
{
    atomic_store(&finished, 0);
    for (long k = 0; k < connections; k++) {
        int c = accept(lfd, NULL, NULL);
        pthread_t t;
        pthread_create(&t, NULL, handle_thread, (void *)(intptr_t)c);
        pthread_detach(t);                       /* nobody joins it: it cleans up alone */
    }
    while (atomic_load(&finished) < connections)
        sched_yield();                           /* let the last threads finish */
}

#define MAXC 1024
struct conn { int fd; size_t len; char buf[260]; };

void serve_poll(int lfd, long connections)
{
    static struct pollfd p[MAXC + 1];
    static struct conn st[MAXC + 1];
    int n = 1;
    long accepted = 0, done = 0;
    p[0] = (struct pollfd){.fd = lfd, .events = POLLIN};
    while (done < connections) {
        poll(p, n, -1);                          /* sleep until some descriptor is ready */
        if ((p[0].revents & POLLIN) && accepted < connections && n <= MAXC) {
            int c = accept(lfd, NULL, NULL);     /* a new connection: watch it too */
            p[n] = (struct pollfd){.fd = c, .events = POLLIN};
            st[n] = (struct conn){.fd = c};
            n++, accepted++;
        }
        for (int i = n - 1; i >= 1; i--) {
            if (!(p[i].revents & (POLLIN | POLLHUP)))
                continue;
            struct conn *s = &st[i];
            ssize_t k = recv(s->fd, s->buf + s->len, sizeof s->buf - s->len, 0);
            const char *msg;
            uint32_t len;
            if (k > 0)
                s->len += k;
            if (k > 0 && !unframe(s->buf, s->len, &msg, &len) && s->len < sizeof s->buf)
                continue;                        /* request not complete yet: wait */
            if (k > 0 && unframe(s->buf, s->len, &msg, &len)) {
                char reply[256];
                send_msg(s->fd, reply, directory_answer(msg, len, reply, sizeof reply));
            }
            close(s->fd);                        /* answered, or broken: forget it */
            p[i] = p[n - 1], st[i] = st[n - 1];
            n--, done++;
        }
    }
}

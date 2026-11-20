/* loadtest.c: 8 client threads, each making 500 connections with one request, against
   each server design in turn. */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#include "directory.h"
#include "net.h"
#include "servers.h"

#define CLIENTS 8
#define EACH 500
#define PORT 44167

static long failures;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

/* Like tcp_connect, but the client socket is marked SO_REUSEADDR before it connects. The
   client closes first, so each of its 4000 connections leaves an ephemeral port in TIME_WAIT
   for a minute; marked this way, those ports do not block a later server that binds one. */
static int connect_reusable(int port)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0), one = 1;
    struct sockaddr_in a = {.sin_family = AF_INET, .sin_port = htons(port),
                            .sin_addr.s_addr = htonl(INADDR_LOOPBACK)};
    if (fd < 0)
        return -1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    if (connect(fd, (struct sockaddr *)&a, sizeof a) != 0) {
        close(fd);
        return -1;
    }
    return fd;
}

static void *client(void *arg)
{
    long id = (long)arg, bad = 0;
    for (int k = 0; k < EACH; k++) {
        char req[32], reply[256];
        int n = snprintf(req, sizeof req, "who %ld", 1 + (id * EACH + k) % 120);
        int fd = connect_reusable(PORT);
        if (fd < 0 || send_msg(fd, req, n) != 0 || recv_msg(fd, reply, sizeof reply) <= 0)
            bad++;
        if (fd >= 0)
            close(fd);
    }
    pthread_mutex_lock(&m);
    failures += bad;
    pthread_mutex_unlock(&m);
    return NULL;
}

static double run(void (*serve)(int, long))
{
    int lfd = tcp_listen(PORT);
    pid_t server = fork();
    if (server == 0) {                           /* the server, in its own process */
        serve(lfd, CLIENTS * EACH);
        _exit(0);
    }
    close(lfd);
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    pthread_t t[CLIENTS];
    for (long i = 0; i < CLIENTS; i++)
        pthread_create(&t[i], NULL, client, (void *)i);
    for (int i = 0; i < CLIENTS; i++)
        pthread_join(t[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &b);
    waitpid(server, NULL, 0);
    return (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
}

int main(void)
{
    if (directory_load("people.csv", "streets.csv") <= 0)
        return 1;
    struct { const char *name; void (*serve)(int, long); } d[] = {
        {"process per connection", serve_fork},
        {"thread per connection", serve_threads},
        {"event loop (poll)", serve_poll},
    };
    printf("%-24s %8s %10s\n", "design", "seconds", "requests/s");
    for (int i = 0; i < 3; i++) {
        double s = run(d[i].serve);
        printf("%-24s %8.3f %10.0f\n", d[i].name, s, CLIENTS * EACH / s);
    }
    printf("failed requests: %ld\n", failures);
    return 0;
}

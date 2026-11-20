/* partial_recv.c: one send of 1 MiB; how many recv calls does it take to receive? */
// capture: with=net.c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

#include "net.h"

#define SIZE (1 << 20)

int main(void)
{
    int lfd = tcp_listen(44161);
    if (fork() == 0) {                           /* the sender */
        char *data = calloc(SIZE, 1);
        int fd = tcp_connect(44161);
        ssize_t sent = send(fd, data, SIZE, 0);  /* one call */
        printf("sender: one send call returned %zd\n", sent);
        close(fd);
        exit(0);
    }
    int c = accept(lfd, NULL, NULL);
    char *buf = malloc(SIZE);
    long calls = 0, total = 0, first = 0;
    ssize_t n;
    while ((n = recv(c, buf, SIZE, 0)) > 0) {    /* ask for everything every time */
        if (calls++ == 0)
            first = n;
        total += n;
    }
    wait(NULL);
    printf("receiver: %ld bytes in all\n", total);
    printf("the first recv returned less than all: %s\n", first < total ? "yes" : "no");
    printf("more than one recv call: %s\n", calls > 1 ? "yes" : "no");
    return 0;
}

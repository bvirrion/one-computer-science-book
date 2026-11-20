/* directory_server.c: the directory service. Usage: directory_server port design n */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "directory.h"
#include "net.h"
#include "servers.h"

int main(int argc, char **argv)
{
    if (argc != 4 || directory_load("people.csv", "streets.csv") <= 0) {
        fprintf(stderr, "usage: directory_server port fork|threads|poll connections\n");
        return 2;
    }
    int lfd = tcp_listen(atoi(argv[1]));
    if (lfd < 0) {
        perror("listen");
        return 1;
    }
    long n = atol(argv[3]);
    if (strcmp(argv[2], "fork") == 0)
        serve_fork(lfd, n);
    else if (strcmp(argv[2], "threads") == 0)
        serve_threads(lfd, n);
    else
        serve_poll(lfd, n);
    return 0;
}

/* count_server.c: a thread per client; each line received is answered with the number of
   lines received from all clients so far (exercise 9). */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>

#include "../listings/net.h"
#include "linereader.h"

static long lines;                               /* shared by every client's thread */
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static void *client_thread(void *arg)
{
    int c = (int)(intptr_t)arg;
    struct linereader r;
    lr_init(&r, c);
    char line[256], reply[32];
    while (lr_line(&r, line, sizeof line) >= 0) {
        pthread_mutex_lock(&m);
        long now = ++lines;                      /* read and change under the lock */
        pthread_mutex_unlock(&m);
        int n = snprintf(reply, sizeof reply, "%ld\n", now);
        if (send_all(c, reply, n) != 0)
            break;
    }
    close(c);
    return NULL;
}

long count_serve(int lfd, int clients)          /* serve that many clients, then return */
{
    pthread_t t[64];
    int k = 0;
    for (; k < clients && k < 64; k++) {
        int c = accept(lfd, NULL, NULL);
        pthread_create(&t[k], NULL, client_thread, (void *)(intptr_t)c);
    }
    for (int i = 0; i < k; i++)
        pthread_join(t[i], NULL);
    return lines;
}

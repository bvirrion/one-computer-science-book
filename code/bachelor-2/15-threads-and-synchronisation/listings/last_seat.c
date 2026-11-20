/* last_seat.c: two booking windows, one seat left. */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>
#include <time.h>

static int seats_left = 1;                       /* shared by both windows */

static void pause_ms(long ms)
{
    struct timespec t = {ms / 1000, (ms % 1000) * 1000000L};
    nanosleep(&t, NULL);
}

struct window {
    const char *name;
    long delay_ms;                               /* when the customer arrives */
    int sold;                                    /* the seat sold, or 0 */
};

static void *sell(void *arg)
{
    struct window *w = arg;
    pause_ms(w->delay_ms);
    if (seats_left > 0) {                        /* check ... */
        int seat = seats_left;
        pause_ms(50);                            /* the clerk prints the ticket */
        seats_left = seat - 1;                   /* ... then sell */
        w->sold = seat;
    }
    return NULL;
}

int main(void)
{
    struct window w[2] = {{"A", 0, 0}, {"B", 10, 0}};
    pthread_t t[2];
    for (int i = 0; i < 2; i++)
        pthread_create(&t[i], NULL, sell, &w[i]);
    for (int i = 0; i < 2; i++)
        pthread_join(t[i], NULL);
    for (int i = 0; i < 2; i++)
        printf("window %s sold seat %d\n", w[i].name, w[i].sold);
    printf("seats left: %d\n", seats_left);
    return 0;
}

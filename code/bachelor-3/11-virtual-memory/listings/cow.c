/* cow.c -- fork shares the parent's pages with the child; the first write to each page in
   the child copies it. The minor page faults counted by getrusage show when. */
#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <unistd.h>

#define PAGES 4096                                     /* 16 MiB */

static long faults(void)
{
    struct rusage u;
    getrusage(RUSAGE_SELF, &u);
    return u.ru_minflt;                                /* minor faults so far */
}

static void report(const char *who, long since)
{
    printf("%-34s %5ld faults\n", who, faults() - since);
}

int main(void)
{
    char *buf = mmap(NULL, PAGES * 4096L, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(buf, PAGES * 4096L, MADV_NOHUGEPAGE);      /* 4 KiB pages only */
    long f0 = faults();
    memset(buf, 1, PAGES * 4096L);                     /* the parent touches every page */
    report("parent, first touch of every page:", f0);
    fflush(stdout);
    if (fork() == 0) {
        volatile long sum = 0;
        long f = faults();
        for (long i = 0; i < PAGES; i++) sum += buf[i * 4096];
        report("child, reads every page:", f);
        f = faults();
        for (long i = 0; i < PAGES; i++) buf[i * 4096] = 2;
        report("child, writes every page:", f);
        f = faults();
        for (long i = 0; i < PAGES; i++) buf[i * 4096] = 3;
        report("child, writes every page again:", f);
        return 0;
    }
    wait(NULL);
    printf("parent, after the child: buf[0] = %d, %d pages of %d bytes\n", buf[0], PAGES, 4096);
    return 0;
}

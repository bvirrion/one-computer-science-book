/* cow_test.c: exercise 9. The child writes every other page, reads every page, then
   writes every page: about PAGES / 2 faults, then none, then PAGES / 2. */
#define _DEFAULT_SOURCE
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <unistd.h>

#define PAGES 1024

static long faults(void)
{
    struct rusage u;
    getrusage(RUSAGE_SELF, &u);
    return u.ru_minflt;
}

static int near(long got, long want) { return got >= want && got <= want + 4; }

int main(void)
{
    char *buf = mmap(NULL, PAGES * 4096L, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(buf, PAGES * 4096L, MADV_NOHUGEPAGE);
    memset(buf, 1, PAGES * 4096L);
    pid_t pid = fork();
    if (pid == 0) {
        volatile long sum = 0;
        long f = faults();
        for (long i = 0; i < PAGES; i += 2) buf[i * 4096] = 2;
        long half = faults() - f;
        f = faults();
        for (long i = 0; i < PAGES; i++) sum += buf[i * 4096];
        long reads = faults() - f;
        f = faults();
        for (long i = 0; i < PAGES; i++) buf[i * 4096] = 3;
        long all = faults() - f;
        return !(near(half, PAGES / 2) && near(reads, 0) && near(all, PAGES / 2));
    }
    int status;
    waitpid(pid, &status, 0);
    assert(WIFEXITED(status) && WEXITSTATUS(status) == 0);
    printf("cow: exercise 9 counts hold\n");
    return 0;
}

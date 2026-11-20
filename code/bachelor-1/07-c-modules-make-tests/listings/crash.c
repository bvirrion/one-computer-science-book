// crash.c: a search that walks off a list of stations.
#include <stdio.h>
#include <string.h>

struct station {
    const char *name;
    struct station *next;
};

int altitude_rank(const struct station *s, const char *name)
{
    int rank = 0;
    while (strcmp(s->name, name) != 0) {    // no test for the end of the list
        s = s->next;
        rank++;
    }
    return rank;
}

int main(void)
{
    struct station r = {"Riverside", NULL}, h = {"Hilltop", &r};
    printf("Riverside: %d\n", altitude_rank(&h, "Riverside"));
    fflush(stdout);
    printf("Harbour: %d\n", altitude_rank(&h, "Harbour"));
    return 0;
}

/* directory.c: answers "who <id>" and "street <name>" from the town's tables. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "directory.h"

#define MAXP 200
#define MAXS 64

static struct { char first[32], last[32]; int born, street; } person[MAXP];
static char street[MAXS][40];
static int npeople;

int directory_load(const char *people_csv, const char *streets_csv)
{
    char line[256];
    FILE *f = fopen(streets_csv, "r");
    if (!f)
        return -1;
    if (!fgets(line, sizeof line, f))            /* the header */
        return fclose(f), -1;
    int id;
    char name[40];
    while (fgets(line, sizeof line, f))
        if (sscanf(line, "%d,%39[^,]", &id, name) == 2 && id > 0 && id < MAXS)
            strcpy(street[id], name);
    fclose(f);
    if (!(f = fopen(people_csv, "r")))
        return -1;
    if (!fgets(line, sizeof line, f))
        return fclose(f), -1;
    while (npeople < MAXP && fgets(line, sizeof line, f)) {
        int pid;
        if (sscanf(line, "%d,%31[^,],%31[^,],%d,%d", &pid, person[npeople].first,
                   person[npeople].last, &person[npeople].born, &person[npeople].street) == 5)
            npeople++;
    }
    fclose(f);
    return npeople;
}

size_t directory_answer(const char *req, size_t n, char *out, size_t cap)
{
    char q[128];
    if (n >= sizeof q)
        return snprintf(out, cap, "error: request too long");
    memcpy(q, req, n);
    q[n] = '\0';
    int id;
    if (sscanf(q, "who %d", &id) == 1) {
        if (id < 1 || id > npeople)
            return snprintf(out, cap, "error: no person %d", id);
        int i = id - 1;
        return snprintf(out, cap, "%s %s, born %d, %s", person[i].first, person[i].last,
                        person[i].born, street[person[i].street]);
    }
    if (strncmp(q, "street ", 7) == 0) {
        int count = 0;
        for (int i = 0; i < npeople; i++)
            count += strcmp(street[person[i].street], q + 7) == 0;
        return snprintf(out, cap, "%s: %d people", q + 7, count);
    }
    return snprintf(out, cap, "error: unknown request");
}

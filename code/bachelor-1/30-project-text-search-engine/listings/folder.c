// folder.c: list a folder's *.txt files; the sort gives every run the same numbering.
#define _POSIX_C_SOURCE 200809L
#include "folder.h"

#include <dirent.h>
#include <stdlib.h>
#include <string.h>

static int by_name(const void *a, const void *b) {
    return strcmp(*(char *const *)a, *(char *const *)b);
}

int folder_list(Folder *f, const char *dir) {
    *f = (Folder){0};
    DIR *d = opendir(dir);
    if (d == NULL)
        return -1;
    for (struct dirent *de; (de = readdir(d)) != NULL;) {
        size_t k = strlen(de->d_name);
        if (k > 4 && strcmp(de->d_name + k - 4, ".txt") == 0) {
            f->names = realloc(f->names, (f->n + 1) * sizeof *f->names);
            f->names[f->n++] = strdup(de->d_name);
        }
    }
    closedir(d);
    qsort(f->names, f->n, sizeof *f->names, by_name);
    return 0;
}

void folder_free(Folder *f) {
    for (int i = 0; i < f->n; i++)
        free(f->names[i]);
    free(f->names);
}

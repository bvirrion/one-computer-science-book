// naive.c: naive DIR WORD... -- the same answers as search, by scanning every file.
#include <stdio.h>

#include "folder.h"
#include "query.h"
#include "scan.h"
#include "tokenize.h"

#define MAX_TERMS 16
#define SHOWN 10

int main(int argc, char **argv) {
    Folder f;
    if (argc < 3 || folder_list(&f, argv[1]) != 0) {
        fprintf(stderr, "usage: naive DIR WORD...\n");
        return 2;
    }
    char words[MAX_TERMS][MAX_WORD], *terms[MAX_TERMS];
    int n = split_words(argc - 2, argv + 2, words, terms, MAX_TERMS);
    Hit top[SHOWN];
    int shown, matches = scan_and(argv[1], &f, terms, n, top, SHOWN, &shown);
    if (matches < 0)
        fprintf(stderr, "naive: out of memory\n");
    else
        print_hits(f.names, top, shown, matches);
    folder_free(&f);
    return matches > 0 ? 0 : matches == 0 ? 1 : 2;
}

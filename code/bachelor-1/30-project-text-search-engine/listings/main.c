// main.c: search DIR [WORD...] -- index the folder's texts, answer one AND query.
// Exit status: 0 some document matches (or no word: the index's statistics),
// 1 none matches, 2 usage, a folder that cannot be read, or no memory left.
#include <stdio.h>

#include "index.h"
#include "query.h"
#include "tokenize.h"

#define MAX_TERMS 16
#define SHOWN 10

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: search DIR [WORD...]\n");
        return 2;
    }
    Index ix;
    if (index_init(&ix) != 0 || index_directory(&ix, argv[1]) != 0) {
        fprintf(stderr, "search: cannot read the texts of %s\n", argv[1]);
        index_free(&ix);
        return 2;
    }
    char words[MAX_TERMS][MAX_WORD], *terms[MAX_TERMS];
    int n = split_words(argc - 2, argv + 2, words, terms, MAX_TERMS), status = 0;
    if (n == 0) {
        printf("%d documents, %zu distinct words, %ld postings, %zu bytes\n", ix.ndocs,
               ix.nwords, ix.npostings, index_memory(&ix));
    } else {
        Hit top[SHOWN];
        int shown, matches = query_and(&ix, terms, n, top, SHOWN, &shown);
        if (matches < 0) {
            fprintf(stderr, "search: out of memory\n");
            status = 2;
        } else {
            print_hits(ix.names, top, shown, matches);
            status = matches > 0 ? 0 : 1;
        }
    }
    index_free(&ix);
    return status;
}

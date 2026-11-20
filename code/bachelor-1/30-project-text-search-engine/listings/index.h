// index.h: the inverted index, a hash table from words to posting lists.
#ifndef INDEX_H
#define INDEX_H
#include <stddef.h>

typedef struct {
    int doc;    // a document number, 0, 1, 2, ... in the order indexed
    int count;  // how many times the word occurs in it
} Posting;

typedef struct {
    Posting *items;  // sorted by document, one posting per document
    int size, cap;
} PostingList;

typedef struct Entry {
    char *word;
    PostingList list;
    struct Entry *next;  // the next entry of the same bucket
} Entry;

typedef struct {
    Entry **buckets;
    size_t nbuckets, nwords;  // the table doubles when nwords exceeds nbuckets
    long npostings;
    char **names;  // names[d]: the file name of document d
    int ndocs, cap_docs;
} Index;

void index_init(Index *ix);
int index_add_text(Index *ix, const char *name, const char *text, size_t len);
int index_directory(Index *ix, const char *dir);  // every *.txt, by name; -1 on error
const PostingList *index_lookup(const Index *ix, const char *word);
size_t index_memory(const Index *ix);  // bytes allocated, counted
void index_free(Index *ix);
#endif

// exercises.h: the solutions of the chapter's programming exercises.
#ifndef EXERCISES_H
#define EXERCISES_H
#include "../listings/index.h"
#include "../listings/topk.h"

// Exercise 7: documents that contain at least one term, scored by tf-idf.
int query_or(const Index *ix, char **terms, int nterms, Hit *top, int k, int *nfound);
// Exercise 8: how many documents contain every term, for search --count.
int count_and(const Index *ix, char **terms, int nterms);
// Exercise 10: documents containing the words consecutively; docs[] gets them in order.
int phrase_docs(const char **texts, int ndocs, char **words, int nwords, int *docs);
// Exercise 12: the index to a binary file and back; 0 on success.
int index_save(const Index *ix, const char *path);
int index_load(Index *ix, const char *path);
#endif

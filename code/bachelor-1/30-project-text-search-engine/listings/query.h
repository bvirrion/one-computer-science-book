// query.h: AND queries on the index, scored by tf-idf, the best k kept.
#ifndef QUERY_H
#define QUERY_H
#include "index.h"
#include "topk.h"

// The documents that contain every term; the best k go into top, best first, and
// *nfound gets how many there are. Returns the number of matching documents.
int query_and(const Index *ix, char **terms, int nterms, Hit *top, int k, int *nfound);

// tf-idf of a document for the terms, summed in the order given, as the scan does too.
double tfidf(int ndocs, const int *tf, const int *df, int nterms);
// Print the hits as both programs do: the count, then score and file name, best first.
void print_hits(char **names, const Hit *top, int shown, int matches);
#endif

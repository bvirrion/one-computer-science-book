// topk.h: the k best hits of a stream, in a min-heap of size k.
#ifndef TOPK_H
#define TOPK_H

typedef struct {
    double score;
    int doc;
} Hit;

typedef struct {
    Hit *heap;  // heap[0] is the worst of the hits kept
    int size, k;
} TopK;

int hit_better(Hit a, Hit b);  // a higher score, or the same score and a smaller doc
void topk_init(TopK *t, Hit *storage, int k);
void topk_push(TopK *t, Hit h);
int topk_sorted(TopK *t);  // sorts the storage best first; returns the number of hits
#endif

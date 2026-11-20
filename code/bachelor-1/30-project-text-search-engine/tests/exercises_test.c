// test-with: ../listings/tokenize.c ../listings/folder.c ../listings/index.c ../listings/query.c ../listings/topk.c ../exercises/or_query.c ../exercises/count.c ../exercises/phrase.c ../exercises/persist.c
// Tests of the exercises: OR queries and counts against brute force, phrases, and a
// save-and-load round trip.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../exercises/exercises.h"
#include "query.h"
#include "tokenize.h"

static int failed, checks;
#define CHECK(c) (checks++, (c) ? (void)0 : (void)(failed++, printf("FAIL line %d: %s\n", __LINE__, #c)))

static const char *TEXTS[] = {"red fish blue fish", "one fish two fish", "red car",
                              "blue car, red fish", "the old red barn", "fish"};
enum { N = 6 };

static int contains(const char *text, const char *word) {
    char w[MAX_WORD];
    size_t pos = 0, len = strlen(text);
    while (next_word(text, len, &pos, w) > 0)
        if (strcmp(w, word) == 0)
            return 1;
    return 0;
}

int main(void) {
    Index ix;
    index_init(&ix);
    for (int d = 0; d < N; d++)
        index_add_text(&ix, "t", TEXTS[d], strlen(TEXTS[d]));
    char *vocab[] = {"red", "fish", "blue", "car", "barn", "zebra"};
    for (int a = 0; a < 6; a++)
        for (int b = 0; b < 6; b++) {
            char *q[] = {vocab[a], vocab[b]};
            int and_n = 0, or_n = 0;
            for (int d = 0; d < N; d++) {
                and_n += contains(TEXTS[d], q[0]) && contains(TEXTS[d], q[1]);
                or_n += contains(TEXTS[d], q[0]) || contains(TEXTS[d], q[1]);
            }
            Hit top[10];
            int shown;
            CHECK(count_and(&ix, q, 2) == and_n);
            CHECK(query_or(&ix, q, 2, top, 10, &shown) == or_n && shown == or_n);
        }
    char *p1[] = {"red", "fish"}, *p2[] = {"fish", "red"}, *p3[] = {"fish"};
    int docs[N];
    CHECK(phrase_docs(TEXTS, N, p1, 2, docs) == 2 && docs[0] == 0 && docs[1] == 3);
    CHECK(phrase_docs(TEXTS, N, p2, 2, docs) == 0);  // "fish blue", never "fish red"
    CHECK(phrase_docs(TEXTS, N, p3, 1, docs) == 4);
    const char *path = "persist_test.bin";
    Index back;
    CHECK(index_save(&ix, path) == 0 && index_load(&back, path) == 0);
    remove(path);
    CHECK(back.ndocs == ix.ndocs && back.nwords == ix.nwords && back.npostings == ix.npostings);
    for (int a = 0; a < 5; a++) {
        const PostingList *x = index_lookup(&ix, vocab[a]), *y = index_lookup(&back, vocab[a]);
        CHECK(y != NULL && x->size == y->size &&
              memcmp(x->items, y->items, x->size * sizeof *x->items) == 0);
    }
    index_free(&back);
    CHECK(index_load(&back, "no-such-file.bin") == -1);
    index_free(&back);
    index_free(&ix);
    printf("%d checks, %d failed\n", checks, failed);
    return failed != 0;
}

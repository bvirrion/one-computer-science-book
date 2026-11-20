// test-with: tokenize.c folder.c index.c query.c topk.c
// Unit tests of the tokenizer, the index, the top-k heap and the AND query.
#include <stdio.h>
#include <string.h>

#include "index.h"
#include "query.h"
#include "tokenize.h"
#include "topk.h"

static int failed, checks;
#define CHECK(c) (checks++, (c) ? (void)0 : (void)(failed++, printf("FAIL line %d: %s\n", __LINE__, #c)))

static void test_tokenizer(void) {
    const char *t = "Don't  STOP--now: caf\xc3\xa9 x2y\n";
    const char *want[] = {"don", "t", "stop", "now", "caf", "x", "y"};
    char w[MAX_WORD];
    size_t pos = 0, len = strlen(t);
    int n = 0;
    while (next_word(t, len, &pos, w) > 0)
        CHECK(n < 7 && strcmp(w, want[n++]) == 0);
    CHECK(n == 7);
    char longw[100];  // a word of 99 letters is cut to 63
    memset(longw, 'a', 99);
    pos = 0;
    CHECK(next_word(longw, 99, &pos, w) == MAX_WORD - 1 && pos == 99);
    pos = 0;
    CHECK(next_word("end", 3, &pos, w) == 3 && strcmp(w, "end") == 0);  // no final byte
}

static void test_index_and_query(void) {
    Index ix;
    index_init(&ix);
    const char *docs[] = {"the cat sat", "the cat and the dog", "a dog", "Cat cat CAT"};
    for (int d = 0; d < 4; d++) {
        char name[8];
        snprintf(name, sizeof name, "d%d", d);
        index_add_text(&ix, name, docs[d], strlen(docs[d]));
    }
    const PostingList *cat = index_lookup(&ix, "cat");
    CHECK(cat != NULL && cat->size == 3 && cat->items[2].doc == 3 && cat->items[2].count == 3);
    CHECK(index_lookup(&ix, "the")->items[1].count == 2);
    CHECK(index_lookup(&ix, "bird") == NULL && ix.nwords == 6 && ix.npostings == 10);
    char *q[] = {"cat", "the"};
    Hit top[10];
    int shown, m = query_and(&ix, q, 2, top, 10, &shown);
    CHECK(m == 2 && shown == 2 && top[0].doc == 1);  // d1: cat once, the twice
    char *none[] = {"cat", "bird"};
    CHECK(query_and(&ix, none, 2, top, 10, &shown) == 0 && shown == 0);
    for (int i = 0; i < 3000; i++) {  // enough words to make the table grow
        char w[16];
        snprintf(w, sizeof w, "w%d", i);
        index_add_text(&ix, "big", w, strlen(w));
    }
    CHECK(ix.nbuckets >= ix.nwords && index_lookup(&ix, "cat")->size == 3);
    index_free(&ix);
}

static void test_topk(void) {
    Hit store[3];
    TopK t;
    topk_init(&t, store, 3);
    double scores[] = {5, 1, 9, 7, 3, 9, 2};
    for (int i = 0; i < 7; i++)
        topk_push(&t, (Hit){scores[i], i});
    CHECK(topk_sorted(&t) == 3);
    CHECK(store[0].doc == 2 && store[1].doc == 5 && store[2].doc == 3);  // 9, 9, 7
}

int main(void) {
    test_tokenizer();
    test_index_and_query();
    test_topk();
    printf("%d checks, %d failed\n", checks, failed);
    return failed != 0;
}

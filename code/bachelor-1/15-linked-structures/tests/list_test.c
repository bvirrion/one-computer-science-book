// test-with: ../listings/list.c ../exercises/reverse.c ../exercises/floyd.c
// Lists: push, insert, remove at every position, reverse, and cycle detection.
#include "list.h"
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>

node *list_reverse(node *head);
bool has_cycle(const node *head);

static node *range(int n) {  // 0 -> 1 -> ... -> n-1
    node *head = NULL;
    for (int x = n - 1; x >= 0; x--) list_push(&head, x);
    return head;
}

int main(void) {
    for (int n = 0; n < 8; n++)
        for (int x = -1; x <= n; x++) {  // remove each value, and absent ones
            node *head = range(n);
            int found = list_remove(&head, x);
            assert(found == (x >= 0 && x < n));
            assert(list_length(head) == (size_t)(n - found));
            int expect = 0;
            for (node *p = head; p != NULL; p = p->next, expect++) {
                if (expect == x) expect++;
                assert(p->value == expect);
            }
            list_free(head);
        }
    node *head = range(5);
    list_insert_after(head->next->next->next->next, 5);  // after the last cell
    head = list_reverse(head);
    int expect = 5;  // six cells: 5, 4, ..., 0
    for (const node *p = head; p != NULL; p = p->next, expect--)
        assert(p->value == expect);
    assert(expect == -1);
    list_free(head);  // the whole list, from its head
    node *one = range(1);  // a list of length 1
    assert(list_reverse(one) == one && one->value == 0 && one->next == NULL);
    list_free(one);
    assert(list_reverse(NULL) == NULL);
    for (int n = 0; n <= 30; n++) {
        static node cells[30];
        for (int i = 0; i < n; i++) cells[i] = (node){i, i + 1 < n ? &cells[i + 1] : NULL};
        assert(!has_cycle(n ? cells : NULL));
        for (int mu = 0; mu < n; mu++) {  // close the list into a cycle at cell mu
            cells[n - 1].next = &cells[mu];
            assert(has_cycle(cells));
        }
    }
    puts("list: ok");
    return 0;
}

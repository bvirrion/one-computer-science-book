// floyd.c: does a list end, or does it run into a cycle? Two pointers, O(1) memory.
#include "list.h"
#include <stdbool.h>

bool has_cycle(const node *head) {
    const node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;        // one step
        fast = fast->next->next;  // two steps
        if (slow == fast) return true;
    }
    return false;  // fast reached the end
}

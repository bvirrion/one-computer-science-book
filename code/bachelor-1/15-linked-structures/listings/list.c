// list.c: the operations on singly linked lists.
#include "list.h"
#include <stdio.h>
#include <stdlib.h>

static node *new_node(int x, node *next) {
    node *n = malloc(sizeof *n);
    if (n == NULL) {
        perror("list");
        exit(1);
    }
    *n = (node){x, next};
    return n;
}

void list_push(node **head, int x) { *head = new_node(x, *head); }

void list_insert_after(node *cell, int x) { cell->next = new_node(x, cell->next); }

int list_remove(node **head, int x) {
    node **link = head;  // the link that points to the cell under examination
    while (*link != NULL && (*link)->value != x) link = &(*link)->next;
    if (*link == NULL) return 0;
    node *dead = *link;
    *link = dead->next;  // redirect the link past the cell, then free it
    free(dead);
    return 1;
}

size_t list_length(const node *head) {
    size_t n = 0;
    for (const node *p = head; p != NULL; p = p->next) n++;
    return n;
}

void list_print(const node *head) {
    for (const node *p = head; p != NULL; p = p->next) printf("%d -> ", p->value);
    printf("NULL\n");
}

void list_free(node *head) {
    while (head != NULL) {
        node *next = head->next;  // read next before the cell is freed
        free(head);
        head = next;
    }
}

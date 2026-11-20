// list.h: singly linked lists of int, handled through a pointer to the first cell.
#ifndef LIST_H
#define LIST_H
#include <stddef.h>

typedef struct node {
    int value;
    struct node *next;  // NULL in the last cell
} node;

void list_push(node **head, int x);       // add x at the front
void list_insert_after(node *cell, int x);  // add x right after cell
int list_remove(node **head, int x);      // remove the first x; returns 1 if found
size_t list_length(const node *head);
void list_print(const node *head);
void list_free(node *head);
#endif

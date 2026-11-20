// count.h: the interface of the counting module.
#ifndef COUNT_H
#define COUNT_H

#define MAX_REPORTS 3

extern long lines, words;
void feed(int c);
void report(const char *title);

#endif

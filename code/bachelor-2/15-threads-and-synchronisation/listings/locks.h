/* locks.h: two locks built from loads and stores only. */
#ifndef LOCKS_H
#define LOCKS_H

#define MAXT 8

void peterson_lock(int i);                       /* i = 0 or 1 */
void peterson_unlock(int i);
void bakery_init(int n);                         /* n threads, numbered 0 to n - 1 */
void bakery_lock(int i);
void bakery_unlock(int i);

#endif

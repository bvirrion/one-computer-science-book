/* journal.c -- the same crashes, with the journal on. */
// capture: scratch with=minifs.c
#define WITH_JOURNAL 1
#include "crash.c"

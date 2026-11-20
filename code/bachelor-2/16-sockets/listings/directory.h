/* directory.h: the town directory, loaded from people.csv and streets.csv. */
#ifndef DIRECTORY_H
#define DIRECTORY_H

#include <stddef.h>

int directory_load(const char *people_csv, const char *streets_csv);
size_t directory_answer(const char *req, size_t n, char *out, size_t cap);

#endif

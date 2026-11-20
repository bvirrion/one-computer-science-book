// scan.h: the naive search, reading every file for every query; the tests' oracle.
#ifndef SCAN_H
#define SCAN_H
#include "folder.h"
#include "topk.h"

int scan_and(const char *dir, const Folder *f, char **terms, int nterms, Hit *top, int k,
             int *nfound);
#endif

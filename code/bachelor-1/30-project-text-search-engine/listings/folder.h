// folder.h: the *.txt files of a folder, sorted by name.
#ifndef FOLDER_H
#define FOLDER_H

typedef struct {
    char **names;
    int n;
} Folder;

int folder_list(Folder *f, const char *dir);  // 0, or -1 if the folder cannot be read
void folder_free(Folder *f);
#endif

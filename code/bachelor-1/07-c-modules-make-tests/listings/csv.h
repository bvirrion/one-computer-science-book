// csv.h: split a line of comma-separated fields, in place.
#ifndef CSV_H
#define CSV_H

// Removes the final newline of line, replaces each comma by a zero byte and stores in fields[] the start of
// each field (empty fields included). Returns the number of fields, or -1 if there are more than max.
int csv_split(char *line, char **fields, int max);

#endif

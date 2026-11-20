/* minish_parse.h: splitting a command line into words. */
#ifndef MINISH_PARSE_H
#define MINISH_PARSE_H

#define MAXARGS 64

int split(char *line, char **argv, int max, int last);

#endif

// weather_csv.c: count the rows, the missing temperatures and the error codes of the town's file.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 2;
    }
    FILE *f = fopen(argv[1], "r");
    if (f == NULL) {
        perror(argv[1]);
        return 1;
    }
    char line[128];
    int rows = 0, missing = 0, codes = 0;
    if (fgets(line, sizeof line, f) == NULL) {         // the header
        fclose(f);
        return 1;
    }
    while (fgets(line, sizeof line, f) != NULL) {
        rows++;
        char *temp = strchr(line, ',');                // after the date
        temp = temp ? strchr(temp + 1, ',') : NULL;    // after the station
        if (temp == NULL)
            continue;
        temp++;
        if (*temp == ',')
            missing++;                                 // an empty field
        else if (strtod(temp, NULL) == -99.0)
            codes++;                                   // the logger's error code
    }
    fclose(f);
    printf("%d rows, %d missing temperatures, %d error codes\n", rows, missing, codes);
    return 0;
}

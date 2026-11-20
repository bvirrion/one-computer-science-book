#!/bin/bash
# count_lines.sh: the number of lines of each CSV file of the current directory.
for f in $(ls *.csv); do
    wc -l $f
done

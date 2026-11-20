#!/bin/bash
# pipelines.sh -- the command lines of exercises 5, 8 and 15, run where the town's CSV files are
tail -n +2 books.csv | wc -l                                            # exercise 5
cut -d, -f3 books.csv | tail -n +2 | sort | uniq -c | sort -n | tail -3  # exercise 8
cut -d, -f2 loans.csv | tail -n +2 | sort | tail -1                      # exercise 15, wrong
cut -d, -f2 loans.csv | tail -n +2 | sort -n | tail -1                   # exercise 15, right

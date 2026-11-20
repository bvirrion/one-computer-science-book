#!/bin/bash
# count_loans.sh -- exercise 14: how many loans has member $1?
# usage: bash count_loans.sh 55   (run where loans.csv is)
if [ $# -ne 1 ]; then
    echo "usage: bash count_loans.sh MEMBER" >&2
    exit 1
fi
cut -d, -f3 loans.csv | tail -n +2 | grep -c -x "$1"

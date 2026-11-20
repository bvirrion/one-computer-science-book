#!/bin/bash
# logstat.sh LOG HOUR: the number of lines and of distinct members in one hour of an access log.
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "usage: $0 LOG HOUR" >&2
    exit 2
fi
log=$1
hour=$2
if ! [[ "$hour" =~ ^[0-2][0-9]$ ]]; then
    echo "$0: hour must have two digits, got '$hour'" >&2
    exit 2
fi
lines=$(grep -c "^.\{11\}$hour:" "$log" || true)
if [ "$lines" -eq 0 ]; then
    echo "no line at hour $hour"
    exit 1
fi
members=$(grep "^.\{11\}$hour:" "$log" | grep -oE 'member=[0-9]+' | sort -u | wc -l)
echo "hour $hour: $lines lines, $members distinct members"

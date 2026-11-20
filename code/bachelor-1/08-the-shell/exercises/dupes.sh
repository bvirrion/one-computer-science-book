#!/bin/bash
# dupes.sh DIR: the groups of files with the same content under DIR, one group per line (exercise 10).
set -euo pipefail

if [ "$#" -ne 1 ] || [ ! -d "$1" ]; then
    echo "usage: $0 DIR" >&2
    exit 2
fi
table=$(mktemp)
trap 'rm -f "$table"' EXIT

# one line per file: CHECKSUM:SIZE PATH (cksum prints the checksum and the size of its input)
find "$1" -type f | sort | while IFS= read -r path; do
    echo "$(cksum < "$path" | tr ' ' ':') $path"
done | sort > "$table"

# every key that occurs twice or more, then the paths that share it
cut -d' ' -f1 "$table" | uniq -d | while read -r key; do
    grep "^$key " "$table" | cut -d' ' -f2- | paste -sd'|'
done

#!/bin/bash
# topk.sh FILE COL K: the K most frequent values of column COL of a CSV file with a header (exercise 7).
set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "usage: $0 FILE COL K" >&2
    exit 2
fi
file=$1
col=$2
k=$3
if ! [[ "$col" =~ ^[1-9][0-9]*$ && "$k" =~ ^[1-9][0-9]*$ ]]; then
    echo "$0: COL and K must be positive integers" >&2
    exit 2
fi
tail -n +2 "$file" | cut -d, -f"$col" | sort | uniq -c | sort -rn | head -n "$k"

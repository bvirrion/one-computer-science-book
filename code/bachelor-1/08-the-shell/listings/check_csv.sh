#!/bin/bash
# check_csv.sh: every CSV file given must have a header and rows with as many fields as the header.
set -euo pipefail

if [ "$#" -eq 0 ]; then
    echo "usage: $0 FILE..." >&2
    exit 2
fi

status=0
for f in "$@"; do
    if [ ! -r "$f" ]; then
        echo "$f: cannot read" >&2
        status=1
        continue
    fi
    commas=$(head -1 "$f" | tr -dc ',')                    # the header's commas, e.g. ",,,,"
    rows=$(tail -n +2 "$f" | wc -l)
    bad=$(tail -n +2 "$f" | tr -dc ',\n' | grep -cvx "$commas" || true)
    if [ "$rows" -eq 0 ] || [ "$bad" -ne 0 ]; then
        echo "$f: $rows rows, $bad with a wrong number of fields"
        status=1
    else
        echo "$f: $rows rows of $(( ${#commas} + 1 )) fields"
    fi
done
exit "$status"

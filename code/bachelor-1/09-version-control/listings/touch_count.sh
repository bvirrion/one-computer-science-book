#!/bin/bash
# touch_count.sh [REPO]: for each file, the number of commits that changed it.
set -euo pipefail
cd "${1:-.}"
git log --format= --name-only --no-merges |
    grep -v '^$' |
    sort | uniq -c |
    sort -k1,1rn -k2,2

# capture: session copy=point.h,segment.h,exo_guard.c
export LC_ALL=C # hidden
gcc -std=c17 -c exo_guard.c 2>&1 | grep -E "error|note" | sed "s/ *$//"

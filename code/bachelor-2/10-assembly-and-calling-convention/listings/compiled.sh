# capture: session copy=sum.c
gcc -O1 -S -o sum.s sum.c
grep -v -E '^\s*\.(cfi|file|text|globl|type|size|ident|section|p2align|align)' sum.s | sed -n '1,/^\.LFE1:/p' | grep -v -E '^(\.LF|\s*$)' | expand -t 8

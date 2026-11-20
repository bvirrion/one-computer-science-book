# trim.sh: keep the lines of a ThreadSanitizer report that name the race; hide addresses.
grep -E "WARNING|of size|#0 sell|Location|SUMMARY|^window|^seats" |
    sed -E 's/ \(pid=[0-9]+\)//; s/ \([a-z_]+\+0x[0-9a-f]+\)//; s/0x[0-9a-f]+/0x.../g'

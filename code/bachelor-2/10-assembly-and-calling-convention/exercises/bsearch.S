# bsearch.S: recursive binary search under the calling convention (exercise 10).
# find(a0 = array, a1 = lo, a2 = hi, a3 = key) -> index of key in a[lo..hi), or -1
        .text
find:   blt  a1, a2, split
        li   a0, -1             # empty range
        ret
split:  addi sp, sp, -16
        sw   ra, 12(sp)
        add  t0, a1, a2
        srai t0, t0, 1          # mid = (lo + hi) / 2, no overflow for these sizes
        slli t1, t0, 2
        add  t1, a0, t1
        lw   t1, 0(t1)          # a[mid]
        beq  t1, a3, found
        blt  a3, t1, left
        addi a1, t0, 1          # search a[mid+1..hi)
        call find
        j    out
left:   mv   a2, t0             # search a[lo..mid)
        call find
        j    out
found:  mv   a0, t0
out:    lw   ra, 12(sp)
        addi sp, sp, 16
        ret
main:   li   a7, 5
        ecall                   # the key
        mv   a3, a0
        la   a0, pages
        li   a1, 0
        li   a2, 7
        addi sp, sp, -16
        sw   ra, 12(sp)
        call find
        li   a7, 1
        ecall
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
        .data
pages:  .word 65, 98, 133, 189, 251, 320, 412

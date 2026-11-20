# bubble_sort.S: sort 16 page counts in place with bubble sort, then print them.
        .data
a:      .word 412, 65, 320, 98, 251, 133, 189, 77, 501, 12, 260, 145, 38, 199, 87, 300
        .text
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        la   a0, a
        li   a1, 16
        call sort
        la   t0, a
        addi t1, t0, 64
show:   lw   a0, 0(t0)          # print the sorted array
        li   a7, 1
        ecall
        li   a0, ' '
        li   a7, 11
        ecall
        addi t0, t0, 4
        bltu t0, t1, show
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret

sort:                           # sort(a0 = array, a1 = n): a leaf
        addi t0, a1, -1         # i = n - 1
outer:  blez t0, done           # for (; i > 0; i--)
        mv   t1, a0             #   p = &a[0]
        slli t2, t0, 2
        add  t2, a0, t2         #   end = &a[i]
inner:  lw   t3, 0(t1)          #   for (; p < end; p++)
        lw   t4, 4(t1)
        ble  t3, t4, keep       #     if (p[0] > p[1]) swap them
        sw   t4, 0(t1)
        sw   t3, 4(t1)
keep:   addi t1, t1, 4
        bltu t1, t2, inner
        addi t0, t0, -1
        j    outer
done:   ret

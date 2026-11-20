# matrix_sum.S: fill a 32 x 32 matrix of words with a[i][j] = i + j, then sum it
# in row order (input 0) or in column order (input 1).
        .data
a:      .space 4096
        .text
main:   la   s0, a
        li   s1, 32             # N
        li   t0, 0              # i
fill_i: li   t1, 0              # j
fill_j: mul  t2, t0, s1
        add  t2, t2, t1
        slli t2, t2, 2
        add  t2, s0, t2         # &a[i][j] = a + 4(iN + j)
        add  t3, t0, t1
        sw   t3, 0(t2)
        addi t1, t1, 1
        blt  t1, s1, fill_j
        addi t0, t0, 1
        blt  t0, s1, fill_i
        li   a7, 5
        ecall                   # the order: 0 rows, 1 columns
        mv   s2, a0
        li   a0, 0              # the sum
        li   t0, 0              # outer counter
outer:  li   t1, 0              # inner counter
inner:  mv   t4, t0             # row order: i = outer, j = inner
        mv   t5, t1
        beqz s2, addr
        mv   t4, t1             # column order: i = inner, j = outer
        mv   t5, t0
addr:   mul  t2, t4, s1
        add  t2, t2, t5
        slli t2, t2, 2
        add  t2, s0, t2
        lw   t3, 0(t2)          # the load the cache sees
        add  a0, a0, t3
        addi t1, t1, 1
        blt  t1, s1, inner
        addi t0, t0, 1
        blt  t0, s1, outer
        li   a7, 1
        ecall
        li   a0, 0
        ret

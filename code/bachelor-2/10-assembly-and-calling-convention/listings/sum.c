/* sum.c: two small functions, compiled for x86-64 to compare with this chapter's RISC-V. */
int sum(const int *a, int n)
{
    int s = 0;
    for (int i = 0; i < n; i++)
        s += a[i];
    return s;
}

int fine_per_day(int kind)
{
    switch (kind) {
    case 0: return 10;
    case 1: return 50;
    case 2: return 5;
    case 3: return 20;
    case 4: return 15;
    default: return 0;
    }
}

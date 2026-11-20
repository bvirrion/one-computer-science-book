// exo_diagram.c: draw the memory at the end of main.
int main(void)
{
    int days[3] = {31, 28, 31};
    int *first = days;
    int *last = &days[2];
    int **which = &last;
    *last = 30;
    *which = first + 1;
    return *last;
}

// exo_frames.c: draw the stack when the marked line runs.
int scale(int v, int factor)
{
    int r = v * factor;
    return r;                            // <-- here, the second time
}

int area(int w, int h)
{
    int s = scale(w, h);
    return s;
}

int main(void)
{
    int a = area(3, 4);
    int b = scale(a, 2);
    return b == 24 ? 0 : 1;
}

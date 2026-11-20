// shapes.c: a tagged union -- a tag says which member of the union is in use.
#include <stdio.h>

enum kind { CIRCLE, RECTANGLE };

struct shape {
    enum kind kind;                                     // the tag
    union {
        struct { double r; } circle;
        struct { double w, h; } rect;
    } as;                                               // one storage, two readings
};

double area(const struct shape *s)
{
    switch (s->kind) {
    case CIRCLE:
        return 3.14159265358979 * s->as.circle.r * s->as.circle.r;
    case RECTANGLE:
        return s->as.rect.w * s->as.rect.h;
    }
    return 0.0;
}

int main(void)
{
    struct shape shapes[] = {
        {.kind = CIRCLE, .as.circle = {.r = 1.0}},
        {.kind = RECTANGLE, .as.rect = {.w = 3.0, .h = 2.0}},
    };
    for (int i = 0; i < 2; i++)
        printf("shape %d: kind %d, area %.4f\n", i, shapes[i].kind, area(&shapes[i]));
    printf("sizeof: union %zu, shape %zu\n", sizeof shapes[0].as, sizeof shapes[0]);
    struct shape bad = shapes[0];
    bad.kind = RECTANGLE;                               // the tag lies: r is read as w, and h as bytes no circle sets
    printf("lying tag: area %g\n", area(&bad));
    return 0;
}

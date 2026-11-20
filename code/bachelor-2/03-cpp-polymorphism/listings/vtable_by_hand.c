// vtable_by_hand.c: what the compiler builds for virtual functions, written in C.
#include <stdio.h>

struct shape;
struct shape_table {                         // one table per class
    double (*area)(const struct shape *);
    const char *(*name)(const struct shape *);
};
struct shape {
    const struct shape_table *table;        // one pointer per object, set by the "constructor"
};
struct circle { struct shape base; double r; };
struct rect { struct shape base; double w, h; };

static double circle_area(const struct shape *s)
{
    const struct circle *c = (const struct circle *)s;   // base is the first member
    return 3.14159265358979 * c->r * c->r;
}
static const char *circle_name(const struct shape *s) { (void)s; return "circle"; }
static double rect_area(const struct shape *s)
{
    const struct rect *r = (const struct rect *)s;
    return r->w * r->h;
}
static const char *rect_name(const struct shape *s) { (void)s; return "rectangle"; }

static const struct shape_table CIRCLE_TABLE = {circle_area, circle_name};
static const struct shape_table RECT_TABLE = {rect_area, rect_name};

int main(void)
{
    struct rect bed = {{&RECT_TABLE}, 12.0, 8.5};
    struct circle pond = {{&CIRCLE_TABLE}, 2.5};
    struct shape *plan[] = {&bed.base, &pond.base};
    for (int i = 0; i < 2; i++) {
        const struct shape *s = plan[i];
        printf("%-9s area %8.2f\n", s->table->name(s), s->table->area(s));  // 2 loads, 1 call
    }
    return 0;
}

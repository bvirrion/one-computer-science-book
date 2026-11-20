/* fines_tables.h (exercise 7): the fines of fines_switch.c with one table per kind, in C. */
#ifndef FINES_TABLES_H
#define FINES_TABLES_H

struct kind_table {                               /* what each kind must provide */
    const char *name;
    int (*fine_cents)(int days_late);
};

struct item {
    const char *title;
    const struct kind_table *kind;                /* replaces the enum tag */
};

static int standard_fine(int d) { return d * 10 < 500 ? d * 10 : 500; }
static int comic_fine(int d) { return d * 25 < 300 ? d * 25 : 300; }
static int study_fine(int d) { return d > 3 ? (d - 3) * 20 : 0; }

static const struct kind_table STANDARD = {"standard", standard_fine};
static const struct kind_table COMIC = {"comic", comic_fine};
static const struct kind_table STUDY = {"study", study_fine};

static inline int fine_cents(const struct item *it, int days_late)
{
    return days_late <= 0 ? 0 : it->kind->fine_cents(days_late);   /* no switch */
}

#endif

// table_suite.h: random puts, gets and deletes against a plain array model.
#include <assert.h>
#include <stdio.h>
#include <string.h>

#define SUITE(PREFIX, T, NEW)                                                          \
    static void PREFIX##_suite(void) {                                                 \
        static int model[3000];                                                        \
        for (int i = 0; i < 3000; i++) model[i] = -1;                                  \
        T *t = NEW;                                                                    \
        unsigned state = 5;                                                            \
        char key[16];                                                                  \
        size_t n = 0;                                                                  \
        for (int r = 0; r < 60000; r++) {                                              \
            state = state * 1103515245u + 12345u;                                      \
            int k = (int)((state >> 8) % 3000), op = (int)((state >> 20) % 3), v = -1; \
            snprintf(key, sizeof key, "name%d", k);                                    \
            if (op == 0) {                                                             \
                PREFIX##_put(t, key, r);                                               \
                n += model[k] < 0, model[k] = r;                                       \
            } else if (op == 1) {                                                      \
                bool found = PREFIX##_delete(t, key);                                  \
                assert(found == (model[k] >= 0));                                      \
                n -= found, model[k] = -1;                                             \
            } else {                                                                   \
                bool found = PREFIX##_get(t, key, &v);                                 \
                assert(found == (model[k] >= 0) && (!found || v == model[k]));         \
            }                                                                          \
            assert(PREFIX##_size(t) == n);                                             \
        }                                                                              \
        PREFIX##_free(t);                                                              \
    }

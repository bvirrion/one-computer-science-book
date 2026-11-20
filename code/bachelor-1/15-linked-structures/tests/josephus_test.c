// The Josephus closed form for k = 2 against a direct simulation on an array of flags.
#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    static char gone[3001];
    for (int n = 1; n <= 3000; n++) {
        memset(gone, 0, sizeof gone);
        int at = 0, last = 0;  // people 0..n-1; count from person 0
        for (int left = n; left > 0; left--) {
            for (int count = 0;; at = (at + 1) % n)
                if (!gone[at] && ++count == 2 - (left == 1)) break;  // last one: itself
            gone[at] = 1, last = at;
        }
        int p = 1;
        while (2 * p <= n) p *= 2;
        assert(last + 1 == 2 * (n - p) + 1);
    }
    puts("josephus: ok");
    return 0;
}

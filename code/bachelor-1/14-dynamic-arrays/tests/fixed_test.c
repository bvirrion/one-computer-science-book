// test-with: ../listings/fixed.c
// The same suite on the fixed-capacity implementation, within its capacity.
#include "vec_suite.h"

int main(void) {
    vec_suite(16);
    puts("fixed: ok");
    return 0;
}

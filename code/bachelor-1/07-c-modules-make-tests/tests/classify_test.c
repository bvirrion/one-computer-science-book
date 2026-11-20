// test-with: ../listings/classify.c
#include "check.h"
#include "classify.h"

int main(void)
{
    CHECK(classify(3, 3, 3) == EQUILATERAL);
    CHECK(classify(3, 4, 5) == SCALENE);
    CHECK(classify(5, 5, 8) == ISOSCELES && classify(8, 5, 5) == ISOSCELES && classify(5, 8, 5) == ISOSCELES);
    CHECK(classify(0, 4, 4) == NOT_A_TRIANGLE && classify(4, -1, 4) == NOT_A_TRIANGLE);
    CHECK(classify(4, 4, 0) == NOT_A_TRIANGLE);
    CHECK(classify(1, 2, 3) == NOT_A_TRIANGLE);          // flat: a + b == c, the boundary
    CHECK(classify(1, 2, 8) == NOT_A_TRIANGLE && classify(8, 1, 2) == NOT_A_TRIANGLE);
    CHECK(classify(1, 8, 2) == NOT_A_TRIANGLE);
    return CHECK_REPORT();
}

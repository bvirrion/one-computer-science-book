// classify.h: the kind of a triangle with integer sides.
#ifndef CLASSIFY_H
#define CLASSIFY_H

enum { NOT_A_TRIANGLE, EQUILATERAL, ISOSCELES, SCALENE };
int classify(int a, int b, int c);

#endif

// evaluator.h: evaluate an expression of digits, +, * and parentheses.
#ifndef EVALUATOR_H
#define EVALUATOR_H

// Evaluates the whole text; sets *ok to 0 on a syntax error (and returns 0).
long evaluate(const char *text, int *ok);

#endif

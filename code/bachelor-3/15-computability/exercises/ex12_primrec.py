"""ex12_primrec.py -- exercise 12: pred, monus and div, built only from zero, succ,
proj, compose and primrec."""
from primrec import add, compose, mul, primrec, proj, succ, zero

pred = primrec(zero, proj(0))  # pred(0) = 0, pred(n + 1) = n
monus_rev = primrec(proj(0), compose(pred, proj(1)))  # y - n, or 0 if negative
monus = compose(monus_rev, proj(1), proj(0))  # monus(x, y) = x - y, cut at 0
one = compose(succ, zero)
is_zero = compose(monus, one, proj(0))  # 1 if x = 0, else 0
eq = compose(is_zero, compose(add, monus, compose(monus, proj(1), proj(0))))
# rem(n, y): n mod y, counting up and wrapping to 0 when the count reaches y
next_r = compose(succ, proj(0))  # next_r(r, y) = r + 1
wrap = compose(monus, next_r, compose(mul, compose(eq, next_r, proj(1)), proj(1)))
rem = primrec(zero, compose(wrap, proj(1), proj(2)))
# div(n, y): add 1 each time the remainder wraps to 0 (y > 0)
wrapped = compose(is_zero, compose(rem, compose(succ, proj(0)), proj(2)))
div = primrec(zero, compose(add, proj(1), wrapped))

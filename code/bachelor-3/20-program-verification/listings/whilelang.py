"""whilelang.py -- the while-language of this chapter, written in Python syntax: integer
variables, assignment, if, while, assert, pass. A loop may begin with invariant(...)
and variant(...) annotations; unknown() is a condition the program does not control.
Machine integers are 8-bit and unsigned: arithmetic wraps modulo 256."""

import ast

BITS, MASK = 8, 255
ALLOWED = (
    ast.Module,
    ast.Assign,
    ast.If,
    ast.While,
    ast.Pass,
    ast.Assert,
    ast.Expr,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Load,
    ast.Store,
    ast.Add,
    ast.Sub,
    ast.FloorDiv,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Eq,
    ast.NotEq,
)


def parse(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED):
            raise SyntaxError(f"not in the while-language: {type(node).__name__}")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.FloorDiv):
            if not (isinstance(node.right, ast.Constant) and node.right.value == 2):
                raise SyntaxError("only // 2 is allowed")
    return tree.body


def annotations(loop):
    """The invariant and variant of a while loop (None when absent), and its body."""
    found, body = {}, list(loop.body)
    while (
        body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Call)
    ):
        call = body.pop(0).value
        found[call.func.id] = call.args[0]
    return found.get("invariant"), found.get("variant"), body


def value(e, env, choose):
    """Big-step evaluation of an expression; integers wrap to 8 bits."""
    match e:
        case ast.Constant(value=c):
            return c
        case ast.Name(id=x):
            return env[x]
        case ast.Call(func=ast.Name(id="unknown")):
            return choose()
        case ast.Call(func=ast.Name(id="implies"), args=[a, b]):
            return (not value(a, env, choose)) or value(b, env, choose)
        case ast.BinOp(left=a, op=op, right=b):
            x, y = value(a, env, choose), value(b, env, choose)
            r = {ast.Add: x + y, ast.Sub: x - y}.get(type(op), x // 2)
            return r & MASK
        case ast.UnaryOp(op=ast.Not(), operand=a):
            return not value(a, env, choose)
        case ast.BoolOp(op=op, values=vs):
            vals = (value(v, env, choose) for v in vs)
            return all(vals) if isinstance(op, ast.And) else any(vals)
        case ast.Compare(left=a, ops=[op], comparators=[b]):
            x, y = value(a, env, choose), value(b, env, choose)
            return {
                ast.Lt: x < y,
                ast.LtE: x <= y,
                ast.Gt: x > y,
                ast.GtE: x >= y,
                ast.Eq: x == y,
                ast.NotEq: x != y,
            }[type(op)]
    raise ValueError(ast.unparse(e))


def run(statements, env, choose=lambda: False, fuel=10_000):
    """Big-step execution; returns the final environment. A failed assert raises."""
    for s in statements:
        match s:
            case ast.Assign(targets=[ast.Name(id=x)], value=e):
                env[x] = value(e, env, choose)
            case ast.If(test=b, body=yes, orelse=no):
                env = run(yes if value(b, env, choose) else no, env, choose, fuel)
            case ast.While(test=b):
                _, _, body = annotations(s)
                while value(b, env, choose):
                    fuel -= 1
                    if fuel < 0:
                        raise RuntimeError("out of fuel")
                    env = run(body, env, choose, fuel)
            case ast.Assert(test=b):
                if not value(b, env, choose):
                    raise AssertionError(f"{ast.unparse(b)}, with {env}")
            case ast.Pass() | ast.Expr():
                pass
    return env

"""A small mutation tester. A mutant is the module with one small change made by
rewriting its syntax tree; the test suite kills it if some test fails."""

import ast
import sys
import types

SWAP = {  # each operator and the operators it is replaced by
    ast.Add: [ast.Sub],
    ast.Sub: [ast.Add],
    ast.Mult: [ast.Add],
    ast.FloorDiv: [ast.Mult],
    ast.Mod: [ast.FloorDiv],
    ast.Lt: [ast.LtE],
    ast.LtE: [ast.Lt],
    ast.Gt: [ast.GtE],
    ast.GtE: [ast.Gt],
    ast.Eq: [ast.NotEq],
    ast.NotEq: [ast.Eq],
    ast.Is: [ast.IsNot],
    ast.IsNot: [ast.Is],
    ast.And: [ast.Or],
    ast.Or: [ast.And],
}


def sites(tree):
    """Every place a mutant can be made, in the order of the source:
    (node, field, index or None, replacement)."""
    found = list(_sites(tree))
    return sorted(found, key=lambda site: (site[0].lineno, site[0].col_offset))


def _sites(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.BinOp, ast.BoolOp)):
            for new in SWAP.get(type(node.op), []):
                yield node, "op", None, new()
        elif isinstance(node, ast.Compare):
            for i, op in enumerate(node.ops):
                for new in SWAP.get(type(op), []):
                    yield node, "ops", i, new()
        elif isinstance(node, ast.Constant) and type(node.value) is int:
            yield node, "value", None, node.value + 1


def mutants(source):
    """Yield (line, before, after, mutant syntax tree), one per site."""
    count = len(sites(ast.parse(source)))
    for k in range(count):
        tree = ast.parse(source)  # a fresh tree for each mutant
        node, field, i, new = sites(tree)[k]
        before = ast.unparse(node)
        if i is None:
            setattr(node, field, new)
        else:
            node.ops[i] = new
        yield node.lineno, before, ast.unparse(node), tree


def load(name, path, tree):
    """Install the mutant as the module `name`, in place of the real one."""
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(tree, str(path), "exec"), module.__dict__)
    sys.modules[name] = module


def analyse(name, path, suite):
    """Run the suite on every mutant; suite() returns True if every test passes."""
    original = sys.modules.get(name)
    results = []
    for line, before, after, tree in mutants(path.read_text()):
        load(name, path, tree)
        try:
            killed = not suite()
        except Exception:
            killed = True  # the mutant crashed the suite itself
        results.append((line, before, after, killed))
    if original is not None:
        sys.modules[name] = original
    return results


def suite_of(test_module, keep=lambda name: True):
    """A suite: import the test module afresh (so that it sees the installed mutant)
    and call each of its test functions that `keep` accepts."""

    def suite():
        sys.modules.pop(test_module, None)
        tests = __import__(test_module)
        for name in dir(tests):
            if name.startswith("test_") and keep(name):
                try:
                    getattr(tests, name)()
                except KeyboardInterrupt:
                    raise
                except BaseException:  # a failed assertion, or pytest's own failures
                    return False
        return True

    return suite

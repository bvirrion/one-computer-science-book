"""One test suite, run on both implementations of the stack."""
import unittest

import stack_linked
import stack_list


class StackTests(unittest.TestCase):
    Stack = None                                # set for each implementation

    def test_new_stack_is_empty(self):
        self.assertTrue(self.Stack().is_empty())

    def test_last_in_first_out(self):
        s = self.Stack()
        for x in [1, 2, 3]:
            s.push(x)
        self.assertEqual([s.pop(), s.pop(), s.pop()], [3, 2, 1])
        self.assertTrue(s.is_empty())

    def test_top_does_not_remove(self):
        s = self.Stack()
        s.push("a")
        self.assertEqual((s.top(), s.top()), ("a", "a"))
        self.assertFalse(s.is_empty())

    def test_empty_stack_refuses(self):
        with self.assertRaises(IndexError):
            self.Stack().pop()
        with self.assertRaises(IndexError):
            self.Stack().top()


for module in [stack_list, stack_linked]:
    suite = unittest.TestSuite()
    for name in unittest.TestLoader().getTestCaseNames(StackTests):
        test = StackTests(name)
        test.Stack = module.Stack
        suite.addTest(test)
    result = unittest.TestResult()
    suite.run(result)
    print(f"{module.__name__:13} {result.testsRun} tests, "
          f"{len(result.failures)} failures, {len(result.errors)} errors")

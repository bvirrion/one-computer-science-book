"""One test suite, run on both implementations of the queue."""
import unittest

import queue_linked
import queue_two_stacks


class QueueTests(unittest.TestCase):
    Queue = None

    def test_first_in_first_out(self):
        q = self.Queue()
        for x in [1, 2, 3]:
            q.enqueue(x)
        self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3])
        self.assertTrue(q.is_empty())

    def test_mixed_operations(self):
        q, out = self.Queue(), []
        for step in "ab-c--d-":                  # a letter enqueues, - dequeues
            if step == "-":
                out.append(q.dequeue())
            else:
                q.enqueue(step)
        self.assertEqual(out, ["a", "b", "c", "d"])

    def test_reused_after_emptying(self):
        q = self.Queue()
        q.enqueue(1)
        q.dequeue()
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 2)

    def test_empty_queue_refuses(self):
        with self.assertRaises(IndexError):
            self.Queue().dequeue()


for module in [queue_linked, queue_two_stacks]:
    suite = unittest.TestSuite()
    for name in unittest.TestLoader().getTestCaseNames(QueueTests):
        test = QueueTests(name)
        test.Queue = module.Queue
        suite.addTest(test)
    result = unittest.TestResult()
    suite.run(result)
    print(f"{module.__name__:16} {result.testsRun} tests, "
          f"{len(result.failures)} failures, {len(result.errors)} errors")

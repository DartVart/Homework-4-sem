import unittest
from datetime import datetime

from control_tests.control_test1.task1.spy import print_usage_statistic, Spy


class SpyTestCase(unittest.TestCase):
    def test_not_decorated_fun(self):
        def f():
            pass

        with self.assertRaises(ValueError) as context:
            list(print_usage_statistic(f))

        self.assertTrue("Function not decorated with Spy decorator." in str(context.exception))

    def test_fun_without_calls(self):
        @Spy
        def f():
            pass

        self.assertEqual(list(print_usage_statistic(f)), [])

    def test_one_call_check_args(self):
        @Spy
        def f(name):
            print(name)

        f("a")
        actual = [param for time, param in print_usage_statistic(f)]
        self.assertEqual(actual, [{"args": ("a",), "kwargs": {}}])

    def test_two_calls_check_args(self):
        @Spy
        def f(name):
            print(name)

        f("b")
        f("c")
        actual = [param for time, param in print_usage_statistic(f)]
        expected = [{"args": ("b",), "kwargs": {}}, {"args": ("c",), "kwargs": {}}]
        self.assertEqual(actual, expected)

    def test_many_args(self):
        @Spy
        def f(a, b=1, c=100):
            print(a, b, c)

        f(1, b=3, c=10)
        actual = [param for time, param in print_usage_statistic(f)]
        expected = [{"args": (1,), "kwargs": {"b": 3, "c": 10}}]
        self.assertEqual(actual, expected)

    def test_time(self):
        @Spy
        def f(a):
            print(a)

        f(10)
        times_as_str = [time for time, param in print_usage_statistic(f)]
        time = datetime.strptime(times_as_str[0], "%Y-%m-%d %H:%M:%S.%f")
        self.assertTrue(time < datetime.now())

from collections import OrderedDict
from unittest import TestCase

from homeworks.homework2.task2.memioze import memoize

NEGATIVE_SIZE_ERROR_MESSAGE = "Cache size cannot be negative."


class MemoizeTestCase(TestCase):
    def test_negative_size(self):
        with self.assertRaises(ValueError) as context:

            @memoize(size=-1)
            def fun(a):
                return f"-{a}-"

        self.assertTrue(NEGATIVE_SIZE_ERROR_MESSAGE in str(context.exception))

    def test_zero_cache_size(self):
        @memoize(size=0)
        def f(x, y):
            return x ** y

        f(1, 2)
        f(3, 2)
        f(90, 6)

        self.assertTrue(len(f._cache) == 0)

    def test_number_of_runs_is_less_than_cache_size(self):
        @memoize(size=3)
        def f(x, y):
            return x ** y

        f(7, 2)
        f(2, 6)
        self.assertEqual(f._cache, OrderedDict([((7, 2), 49), ((2, 6), 64)]))

    def test_with_named_args(self):
        @memoize(size=2)
        def f(x, y):
            return x ** y

        f(10, 2)
        f(y=3, x=2)
        self.assertEqual(f._cache, OrderedDict([((10, 2), 100), ((("x", 2), ("y", 3)), 8)]))

    def test_runs_more_than_cache_size(self):
        @memoize(size=2)
        def f(x, y):
            return x ** y

        f(7, 2)
        f(2, 6)
        f(5, 1)
        self.assertEqual(f._cache, OrderedDict([((2, 6), 64), ((5, 1), 5)]))

    def test_default_size(self):
        @memoize
        def f(x, y):
            return x ** y

        f(3, 4)
        f(2, 1)
        self.assertTrue(len(f._cache) == 0)

    def test_with_args(self):
        @memoize(size=10)
        def f(*args):
            return sum(args)

        f(1, 4, 7, 8)
        f(3, 5, 7)
        self.assertTrue(f._cache, OrderedDict([((1, 4, 7, 8), 20), ((3, 5, 7), 15)]))

    def test_with_kwargs(self):
        @memoize(size=8)
        def f(**kwargs):
            return "_".join(f"{v}" for v in kwargs.values())

        f(**{"a": 2})
        f(**{"name": "Ivan", "surname": "Petrov"})
        self.assertTrue(
            f._cache, OrderedDict([((("a", 2),), "2"), ((("name", "Ivan"), ("surname", "Petrov")), "Ivan_Petrov")])
        )

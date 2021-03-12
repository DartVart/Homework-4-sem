import unittest

from homeworks.homework2.task1.uncurry import uncurry_explicit
from homeworks.homework2.task1.curry import curry_explicit

from tests.homework2.task1.test_curry import (
    fun_without_args,
    fun_with_one_arg,
    fun_with_several_args,
    fun_with_indefinite_number_of_args,
)

curried_fun_without_args = curry_explicit(fun_without_args, 0)
curried_fun_with_one_arg = curry_explicit(fun_with_one_arg, 1)
curried_fun_with_several_args = curry_explicit(fun_with_several_args, 3)
curried_fun_with_indefinite_number_of_args = curry_explicit(fun_with_indefinite_number_of_args, 5)


class UncurryTestCase(unittest.TestCase):
    def test_without_args(self):
        return self.assertEqual(uncurry_explicit(curried_fun_without_args, 0)(), fun_without_args())

    def test_one_arg(self):
        return self.assertEqual(uncurry_explicit(curried_fun_with_one_arg, 1)(15), fun_with_one_arg(15))

    def test_several_args(self):
        return self.assertEqual(
            uncurry_explicit(curried_fun_with_several_args, 3)("a", "b", "c"), fun_with_several_args("a", "b", "c")
        )

    def test_indefinite_number_of_args(self):
        return self.assertEqual(
            uncurry_explicit(curried_fun_with_indefinite_number_of_args, 5)(6, 7, 8, 9, 0),
            curried_fun_with_indefinite_number_of_args(6, 7, 8, 9, 0),
        )

    def test_negative_arity(self):
        with self.assertRaises(ValueError):
            uncurry_explicit(curried_fun_with_several_args, -10)()

    def test_number_of_arguments_is_greater_than_arity_fun_without_args(self):
        with self.assertRaises(TypeError):
            uncurry_explicit(curried_fun_without_args, 0)(1)

    def test_number_of_arguments_is_greater_than_arity_fun_with_several_args(self):
        with self.assertRaises(TypeError):
            uncurry_explicit(curried_fun_with_several_args, 3)("a", "b", "c", "d")

    def test_number_of_arguments_is_greater_than_arity_fun_with_indefinite_number_of_args(self):
        with self.assertRaises(TypeError):
            uncurry_explicit(curried_fun_with_indefinite_number_of_args, 5)(1, 2, 3, 4, 5, 6, 7)

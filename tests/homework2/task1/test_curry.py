import unittest

from homeworks.homework2.task1.curry import curry_explicit


def fun_without_args():
    return "great value"


def fun_with_one_arg(x: int):
    return x ** 2


def fun_with_several_args(a: str, b: str, c: str):
    return a + b + c


def fun_with_indefinite_number_of_args(*args: int):
    return sum(args)


class CurryTestCase(unittest.TestCase):
    def test_without_arguments(self):
        return self.assertEqual(curry_explicit(fun_without_args, 0)(), fun_without_args())

    def test_one_arg(self):
        return self.assertEqual(curry_explicit(fun_with_one_arg, 1)(100), fun_with_one_arg(100))

    def test_several_arguments(self):
        curried_fun = curry_explicit(fun_with_several_args, 3)
        return self.assertEqual(curried_fun("some")("value")("here"), fun_with_several_args("some", "value", "here"))

    def test_indefinite_number_of_args(self):
        curried_fun = curry_explicit(fun_with_indefinite_number_of_args, 5)
        return self.assertEqual(curried_fun(2)(3)(4)(5)(6), fun_with_indefinite_number_of_args(2, 3, 4, 5, 6))

    def test_intermediate_function(self):
        curried_fun = curry_explicit(fun_with_indefinite_number_of_args, 4)
        intermediate_function = curried_fun(1)(2)
        return self.assertEqual(intermediate_function(3)(4), fun_with_indefinite_number_of_args(1, 2, 3, 4))

    def test_negative_arity(self):
        with self.assertRaises(ValueError):
            curry_explicit(fun_with_several_args, -1)("a")

    def test_number_of_arguments_is_greater_than_arity_indefinite_number_of_args(self):
        with self.assertRaises(TypeError):
            curry_explicit(fun_with_indefinite_number_of_args, 2)(1)(2)(3)

    def test_number_of_arguments_is_greater_than_arity_fun_without_args(self):
        with self.assertRaises(TypeError):
            curry_explicit(fun_without_args, 0)(1)

    def test_double_fun_call(self):
        with self.assertRaises(TypeError):
            curry_explicit(fun_without_args, 0)()()

from unittest import TestCase

from homeworks.homework2.task3.smart_args import Isolated, Evaluated
from homeworks.homework2.task3.smart_args_decorator import smart_args

POSITIONAL_DISABLED_ERROR_MESSAGE = (
    "The default value of the positional parameter is a Smart argument, " "but the ability to handle them is disabled."
)
NO_VALUE_PASSED_WHEN_ISOLATED_ERROR_MESSAGE = "Argument using Isolated has not been assigned a value."
USING_ISOLATED_AND_EVALUATED_ERROR_MESSAGE = "Can't use Evaluated with Isolated."


def check_error_message(context, message: str) -> bool:
    return message in str(context.exception)


@smart_args(need_to_handle_positional_args=True)
def check_isolation_with_named_and_positionals(a, b=4, list_1=Isolated(), *args, c="some", list_2=Isolated(), d=100):
    list_1[0] = -10
    list_2[0] = 100


class TestIsolated(TestCase):
    def test_only_named(self):
        @smart_args
        def check_isolation(*, input_list=Isolated()):
            input_list[0] = -10

        no_mutable_list = [1, 1]
        check_isolation(input_list=no_mutable_list)
        self.assertEqual(no_mutable_list, [1, 1])

    def test_named_and_positionals_check_named(self):
        no_mutable_list_1 = [1, 1]
        no_mutable_list_2 = ["a", "b"]
        check_isolation_with_named_and_positionals(10, 20, no_mutable_list_1, list_2=no_mutable_list_2)
        self.assertEqual(no_mutable_list_2, ["a", "b"])

    def test_named_and_positionals_check_positional(self):
        no_mutable_list_1 = ["a"]
        no_mutable_list_2 = [10, 10]
        check_isolation_with_named_and_positionals(10, 20, no_mutable_list_1, list_2=no_mutable_list_2, d=10)
        self.assertEqual(no_mutable_list_1, ["a"])

    def test_only_positional(self):
        @smart_args(need_to_handle_positional_args=True)
        def check_isolation(input_dict=Isolated()):
            input_dict["a"] = "B"

        no_mutable_dict = {"a": "A"}
        check_isolation(input_dict=no_mutable_dict)
        self.assertEqual(no_mutable_dict, {"a": "A"})

    def test_check_decorated_function_result(self):
        @smart_args
        def check_isolation(*, input_set=Isolated()):
            input_set |= {-10}
            return input_set

        no_mutable_set = {"a"}
        self.assertEqual(check_isolation(input_set=no_mutable_set), {"a", -10})

    def test_positional_arg_when_positionals_disabled(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def check_isolation(x=Isolated()):
                pass

        self.assertTrue(check_error_message(context, POSITIONAL_DISABLED_ERROR_MESSAGE))

    def test_no_value_passed(self):
        @smart_args
        def check_isolation(*, x=Isolated()):
            pass

        with self.assertRaises(ValueError) as context:
            check_isolation()

        self.assertTrue(check_error_message(context, NO_VALUE_PASSED_WHEN_ISOLATED_ERROR_MESSAGE))


def get_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


class TestEvaluated(TestCase):
    def test_only_named(self):
        @smart_args
        def check_evaluation(*, x=Evaluated(get_counter())):
            return x

        check_evaluation()
        self.assertEqual(check_evaluation(), 2)

    def test_named_and_positionals(self):
        @smart_args(need_to_handle_positional_args=True)
        def check_evaluation_with_named_and_positionals(
            b=4, x=Evaluated(get_counter()), *, c="some", y=Evaluated(get_counter()), d=100
        ):
            return x, y

        check_evaluation_with_named_and_positionals("some")
        self.assertEqual(check_evaluation_with_named_and_positionals(), (2, 2))

    def test_only_positional(self):
        @smart_args(need_to_handle_positional_args=True)
        def check_evaluation(a, c=4, x=Evaluated(get_counter())):
            return x

        self.assertEqual(check_evaluation(100, 30), 1)

    def test_positional_arg_when_positionals_disabled(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def check_evaluation(x=Evaluated(get_counter())):
                return x

        self.assertTrue(check_error_message(context, POSITIONAL_DISABLED_ERROR_MESSAGE))

    def test_with_isolated_as_evaluated_argument(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def check_evaluation(*, x=Evaluated(Isolated())):
                return x

        self.assertTrue(check_error_message(context, USING_ISOLATED_AND_EVALUATED_ERROR_MESSAGE))

    def test_with_isolated_class_as_evaluated_argument(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def check_evaluation(*, x=Evaluated(Isolated)):
                return x

        self.assertTrue(check_error_message(context, USING_ISOLATED_AND_EVALUATED_ERROR_MESSAGE))

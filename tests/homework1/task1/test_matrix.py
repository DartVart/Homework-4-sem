import unittest

from homeworks.homework1.task1.matrix import Matrix


class MatrixTestCase(unittest.TestCase):
    def test_trying_to_define_matrix_without_parameters(self):
        with self.assertRaises(ValueError) as context:
            Matrix()

        self.assertTrue("No values passed to define a matrix." in str(context.exception))

    def test_trying_to_define_matrix_with_empty_row(self):
        with self.assertRaises(ValueError) as context:
            Matrix([])

        self.assertTrue("No values passed to define a matrix." in str(context.exception))

    def test_trying_to_define_matrix_with_different_row_sizes(self):
        with self.assertRaises(ValueError) as context:
            Matrix([1.0, 2.0, 3.0], [4.0, 5.0])

        self.assertTrue("Rows in the matrix must be the same length." in str(context.exception))

    def test_size_singled_value_matrix(self):
        self.assertEqual(Matrix([1.0]).size, (1, 1))

    def test_size_simple_matrix(self):
        matrix = Matrix([2.0, 4.0, 6.0], [3.0, 1.0, 9.0])
        self.assertEqual(matrix.size, (2, 3))

    def test_add_different_number_of_columns(self):
        matrix_1 = Matrix([2.0, 4.0, 6.0], [3.0, 1.0, 9.0])

        matrix_2 = Matrix([2.0, 4.0], [3.0, 1.0])

        with self.assertRaises(ValueError) as context:
            matrix_1 + matrix_2

        self.assertTrue("Matrix sizes aren't suitable for addition." in str(context.exception))

    def test_add_different_number_of_rows(self):
        matrix_1 = Matrix([2.0, 4.0, 6.0], [3.0, 1.0, 9.0])

        matrix_2 = Matrix([2.0, 4.0, 5.0], [3.0, 1.0, 40.4], [1.2, -4.04, 3.0])

        with self.assertRaises(ValueError) as context:
            matrix_1 + matrix_2

        self.assertTrue("Matrix sizes aren't suitable for addition." in str(context.exception))

    def test_transpose(self):
        matrix = Matrix([2.0, 4.0, 6.0], [3.0, 1.0, 9.0])

        transposed_matrix = Matrix([2.0, 3.0], [4.0, 1.0], [6.0, 9.0])
        self.assertEqual(matrix, transposed_matrix)

    def test_add_right_sizes_1(self):
        matrix_1 = Matrix([2.0, 4.0, 6.0], [3.0, 1.0, 9.0])

        matrix_2 = Matrix([2.0, 4.0, 5.0], [3.0, 1.0, 5.0])

        result = Matrix([4.0, 8.0, 11.0], [6.0, 2.0, 14.0])

        self.assertEqual(matrix_1 + matrix_2, result)

    def test_add_right_sizes_2(self):
        matrix_1 = Matrix([-435.454, 3452.453], [-323.46547, -231.454], [23425.453, -234.696], [574.23, -234.765])

        matrix_2 = Matrix([23.876, 234.256], [-23.2342, 3453.454], [-5665.13, -3.65396], [1235.432, -56.524])

        result = Matrix(
            [-435.454 + 23.876, 3452.453 + 234.256],
            [-346.699667 - 23.2342, -231.454 + 3453.454],
            [23425.453 - 5665.13, -234.696 - 3.65396],
            [574.23 + 1235.432, -234.765 - 56.524],
        )
        self.assertEqual(matrix_1 + matrix_2, result)

    def test_mul_wrong_sizes(self):
        matrix_1 = Matrix([1.0, 3.0], [3.3, 1.0])

        matrix_2 = Matrix([4.0, 1.0, 3.0], [3.0, 1.0, 1.0], [4.0, 5.0, 1.0])

        with self.assertRaises(ValueError) as context:
            matrix_1 * matrix_2

        self.assertTrue("Matrix sizes aren't suitable for multiplication." in str(context.exception))

    def test_mul_right_sizes_1(self):
        matrix_1 = Matrix([1.0, 3.0], [3.0, 1.0])

        matrix_2 = Matrix([4.0, 1.0, 3.0], [3.0, 1.0, 1.0])

        result = Matrix([13.0, 4.0, 6.0], [15.0, 4.0, 10.0])

        self.assertEqual(matrix_1 * matrix_2, result)

    def test_mul_right_sizes_2(self):
        matrix_1 = Matrix([234.012, -21.203])

        matrix_2 = Matrix([223.023], [-235.235])

        result = Matrix([234.012 * 223.023 + (-235.235) * (-21.203)])

        self.assertEqual(matrix_1 * matrix_2, result)

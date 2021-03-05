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
            Matrix([1, 2, 3], [4, 5])

        self.assertTrue("Rows in the matrix must be the same length." in str(context.exception))

    def test_size_singled_value_matrix(self):
        self.assertEqual(Matrix([1]).size, (1, 1))

    def test_size_simple_matrix(self):
        matrix = Matrix([2, 4, 6], [3, 1, 9])
        self.assertEqual(matrix.size, (2, 3))

    def test_add_different_number_of_columns(self):
        matrix_1 = Matrix([2, 4, 6], [3, 1, 9])

        matrix_2 = Matrix([2, 4], [3, 1])

        with self.assertRaises(ValueError) as context:
            matrix_1 + matrix_2

        self.assertTrue("Matrix sizes aren't suitable for addition." in str(context.exception))

    def test_add_different_number_of_rows(self):
        matrix_1 = Matrix([2, 4, 6], [3, 1, 9])

        matrix_2 = Matrix([2, 4, 5], [3, 1, 40.4], [1.2, -44, 3])

        with self.assertRaises(ValueError) as context:
            matrix_1 + matrix_2

        self.assertTrue("Matrix sizes aren't suitable for addition." in str(context.exception))

    def test_transpose(self):
        matrix = Matrix([2, 4, 6], [3, 1, 9])

        transposed_matrix = Matrix([2, 3], [4, 1], [6, 9]).transpose()
        self.assertEqual(matrix, transposed_matrix)

    def test_add_right_sizes_1(self):
        matrix_1 = Matrix([2, 4, 6], [3, 1, 9])

        matrix_2 = Matrix([2, 4, 5], [3, 1, 5])

        result = Matrix([4, 8, 11], [6, 2, 14])

        self.assertEqual(matrix_1 + matrix_2, result)

    def test_add_right_sizes_2(self):
        matrix_1 = Matrix([-435.454, 3452.453], [-323.46547, -231.454], [23425.453, -234.696], [574.23, -234.765])

        matrix_2 = Matrix([23.876, 234.256], [-23.2342, 3453.454], [-5665.13, -3.65396], [1235.432, -56.524])

        result = Matrix(
            [-435.454 + 23.876, 3452.453 + 234.256],
            [-323.46547 - 23.2342, -231.454 + 3453.454],
            [23425.453 - 5665.13, -234.696 - 3.65396],
            [574.23 + 1235.432, -234.765 - 56.524],
        )
        self.assertEqual(matrix_1 + matrix_2, result)

    def test_mul_wrong_sizes(self):
        matrix_1 = Matrix([1, 3], [3.3, 1])

        matrix_2 = Matrix([4, 1, 3], [3, 1, 1], [4, 5, 1])

        with self.assertRaises(ValueError) as context:
            matrix_1 * matrix_2

        self.assertTrue("Matrix sizes aren't suitable for multiplication." in str(context.exception))

    def test_mul_right_sizes_1(self):
        matrix_1 = Matrix([1, 3], [3, 1])

        matrix_2 = Matrix([4, 1, 3], [3, 1, 1])

        result = Matrix([13, 4, 6], [15, 4, 10])

        self.assertEqual(matrix_1 * matrix_2, result)

    def test_mul_right_sizes_2(self):
        matrix_1 = Matrix([234.012, -21.203])

        matrix_2 = Matrix([223.023], [-235.235])

        result = Matrix([234.012 * 223.023 + (-235.235) * (-21.203)])

        self.assertEqual(matrix_1 * matrix_2, result)

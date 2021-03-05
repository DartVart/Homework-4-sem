import unittest

from homeworks.homework1.task1.vector import Vector


class VectorTestCase(unittest.TestCase):
    def test_trying_to_define_vector_without_parameters(self):
        with self.assertRaises(ValueError) as context:
            Vector()

        self.assertTrue("No values passed to define a vector." in str(context.exception))

    def test_dot_product_different_dimensions(self):
        vector_1 = Vector(1, 4)
        vector_2 = Vector(3)

        with self.assertRaises(ValueError) as context:
            vector_1.dot(vector_2)

        self.assertTrue("The dimensions of the vectors don't match." in str(context.exception))

    def test_dot_product_same_dimensions_1(self):
        vector_1 = Vector(1.3423, -4.43534)
        vector_2 = Vector(3.23423, 6.234231)

        self.assertAlmostEqual(vector_1.dot(vector_2), -23.3096272)

    def test_dot_product_same_dimensions_2(self):
        vector_1 = Vector(1, 3, 101, 3)
        vector_2 = Vector(9, 3, 4, 2)

        self.assertAlmostEqual(vector_1.dot(vector_2), 428)

    def test_norm_zero_vector(self):
        vector = Vector(0, 0, 0)
        self.assertEqual(vector.norm(), 0)

    def test_norm_non_zero_vector_1(self):
        vector = Vector(-2, 5, -7, 1)
        self.assertAlmostEqual(vector.norm(), 8.8881944)

    def test_norm_of_non_zero_vector_2(self):
        vector = Vector(2.234, 3.123)
        self.assertAlmostEqual(vector.norm(), 3.8397767)

    def test_angle_different_dimensions(self):
        vector_1 = Vector(1, 4, 6)
        vector_2 = Vector(3, 3)

        with self.assertRaises(ValueError) as context:
            vector_1.angle(vector_2)

        self.assertTrue("The dimensions of the vectors don't match." in str(context.exception))

    def test_angle_zero_vector(self):
        vector_1 = Vector(1, 4, 6)
        vector_2 = Vector(0, 0, 0)

        with self.assertRaises(ZeroDivisionError) as context:
            vector_1.angle(vector_2)

        self.assertTrue("Can't find angle between zero vector and some other." in str(context.exception))

    def test_angle_same_dimensions_1(self):
        vector_1 = Vector(1, 3, 101, 3)
        vector_2 = Vector(9, 3, 4, 2)

        self.assertAlmostEqual(vector_1.angle(vector_2), 1.1552762)

    def test_angle_same_dimensions_2(self):
        vector_1 = Vector(-4.14, -3.1)
        vector_2 = Vector(-4.05, 24.1)

        self.assertAlmostEqual(vector_1.angle(vector_2), 2.04702992)

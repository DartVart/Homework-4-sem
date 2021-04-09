import unittest
import random

from homeworks.homework5.task1.treap import Treap
from tests.test_utils import check_error_message

TREAP_IS_EMPTY_ERROR_MESSAGE = "Treap is empty."


def get_message_about_key_absence(key):
    return f"Key '{key}' isn't in the treap."


class EmptyTreapTestCase(unittest.TestCase):
    def test_length(self):
        return self.assertEqual(len(Treap()), 0)

    def test_insert(self):
        treap = Treap()
        treap[100] = "100"
        return self.assertTrue(100 in treap)

    def test_remove(self):
        treap = Treap()
        with self.assertRaises(KeyError) as context:
            del treap[100]

        self.assertTrue(check_error_message(context, TREAP_IS_EMPTY_ERROR_MESSAGE))

    def test_get(self):
        treap = Treap()
        with self.assertRaises(KeyError) as context:
            treap[100]

        self.assertTrue(check_error_message(context, TREAP_IS_EMPTY_ERROR_MESSAGE))

    def test_iterator(self):
        self.assertEqual(list(iter(Treap())), [])

    def test_reversed_iterator(self):
        self.assertEqual(list(reversed(Treap())), [])


def get_big_treap():
    treap = Treap()
    keys = set([random.randint(0, 1000) for _ in range(500)])
    for key in keys:
        treap[key] = f"{key}"
    return treap, keys


class NotEmptyTreapTestCase(unittest.TestCase):
    def test_length(self):
        treap, keys = get_big_treap()
        return self.assertEqual(len(treap), len(keys))

    def test_contains(self):
        treap = Treap()
        treap[100] = "a"
        treap[150] = "b"
        treap[-10] = "c"
        return self.assertIn(-10, treap)

    def test_contains_no_key_in_treap(self):
        treap = Treap()
        treap[100] = "a"
        treap[30] = "b"
        treap[20] = "c"
        return self.assertNotIn(-1, treap)

    def test_set_check_iterator(self):
        treap = Treap()
        treap[2.0] = "a"
        treap[10.9] = 3.3
        treap[2.5] = 100
        treap[8.9] = True
        return self.assertEqual(list(iter(treap)), [2.0, 2.5, 8.9, 10.9])

    def test_set_check_get(self):
        treap = Treap()
        treap[100] = "a"
        treap[150] = "b"
        treap[-10] = "c"
        return self.assertEqual(treap[150], "b")

    def test_update_value(self):
        treap = Treap()
        treap["1"] = "a"
        treap["2"] = "b"
        treap["3"] = "c"
        treap["2"] = "updated"
        return self.assertEqual(treap["2"], "updated")

    def test_insert_check_iterator(self):
        treap = Treap()
        treap.insert("a", 1, 2)
        treap.insert("d", 3, 4)
        treap.insert("b", 2, 10)
        treap.insert("c", 2, 1)
        return self.assertEqual(list(iter(treap)), ["a", "b", "c", "d"])

    def test_delete(self):
        treap = Treap()
        treap["b"] = 1
        treap["a"] = 404
        del treap["b"]
        return self.assertNotIn("b", treap)

    def test_insert_and_delete(self):
        treap = Treap()
        treap[100] = "a"
        del treap[100]
        treap[150] = "b"
        treap[-10] = "c"
        del treap[150]
        treap[200] = "d"
        del treap[-10]
        del treap[200]
        return self.assertEqual(len(treap), 0)

    def test_check_iterator(self):
        treap, keys = get_big_treap()
        return self.assertEqual(list(iter(treap)), sorted(list(keys)))

    def test_check_reversed_iterator(self):
        treap, keys = get_big_treap()
        return self.assertEqual(list(reversed(treap)), sorted(list(keys), reverse=True))

    def test_delete_no_key_in_treap(self):
        treap = Treap()
        treap[202] = "a"
        treap[303] = "b"

        with self.assertRaises(KeyError) as context:
            del treap[0]
        self.assertTrue(check_error_message(context, get_message_about_key_absence(0)))

    def test_get_no_key_in_treap(self):
        treap = Treap()
        treap[-100] = 100
        treap[100] = -100

        with self.assertRaises(KeyError) as context:
            treap[101]

        self.assertTrue(check_error_message(context, get_message_about_key_absence(101)))

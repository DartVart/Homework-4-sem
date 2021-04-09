import unittest
import random

from homeworks.homework5.task1.treap_node import TreapNode
from tests.test_utils import check_error_message


def are_priorities_correct(node: "TreapNode"):
    return node is None or (
        (node.left is None or node.left.priority < node.priority)
        and (node.right is None or node.right.priority < node.priority)
        and are_priorities_correct(node.left)
        and are_priorities_correct(node.right)
    )


def check_by_max_value(node: "TreapNode", max_value):
    return node is None or (
        node.key < max_value and check_by_max_value(node.right, max_value) and check_by_max_value(node.left, max_value)
    )


def check_by_min_value(node: "TreapNode", min_value):
    return node is None or (
        min_value < node.key and check_by_min_value(node.right, min_value) and check_by_min_value(node.left, min_value)
    )


def are_keys_correct(node: "TreapNode"):
    return node is None or (
        check_by_max_value(node.left, node.key)
        and check_by_min_value(node.right, node.key)
        and are_keys_correct(node.left)
        and are_keys_correct(node.right)
    )


def get_big_treap_node():
    node = TreapNode(-1, "-1")
    keys = set([random.randint(0, 500) for _ in range(100)])
    for key in keys:
        node = node.get_with_inserted(key, f"{key}")
    return node


class TreapNodeTestCase(unittest.TestCase):
    def test_contains_one_node(self):
        node = TreapNode(10, "10")
        return self.assertTrue(10 in node)

    def test_contains_no_key_in_treap(self):
        node = TreapNode("cdd", 30)
        node = node.get_with_inserted("ab", 23)
        return self.assertFalse("zero" in node)

    def test_contains_several_nodes(self):
        node = TreapNode(10, "10")
        node = node.get_with_inserted(20, "30")
        node = node.get_with_inserted(100, "30")
        return self.assertTrue(100 in node)

    def test_inserting(self):
        node = TreapNode(10, "10")
        node = node.get_with_inserted(20, "20")
        node = node.get_with_inserted(102, "102")
        node = node.get_with_inserted(101, "101")
        node = node.get_with_inserted(2, "2")
        return self.assertTrue(2 in node)

    def test_removing(self):
        node = TreapNode(10, "10")
        node = node.get_with_inserted(20, "20")
        node = node.get_with_removed(10)
        return self.assertFalse(10 in node)

    def test_update(self):
        node = TreapNode(10, "10")
        node = node.get_with_inserted(20, "20")
        node = node.get_with_inserted(-10, "-10")
        node.update(20, 100)
        return self.assertEqual(node.get(20), 100)

    def test_get_one_node(self):
        node = TreapNode(10, "10")
        return self.assertEqual(node.get(10), "10")

    def test_contains_after_removing(self):
        node = TreapNode(5, "20")
        node = node.get_with_inserted(20, "20")
        node = node.get_with_removed(5)
        return self.assertFalse(5 in node)

    def test_big_treap_check_priorities(self):
        node = get_big_treap_node()
        return self.assertTrue(are_priorities_correct(node))

    def test_big_treap_check_keys(self):
        node = get_big_treap_node()
        return self.assertTrue(are_keys_correct(node))

    def test_update_no_key_in_treap(self):
        node = TreapNode(10, "100")
        with self.assertRaises(KeyError) as context:
            node.update(20, "100")

        self.assertTrue(check_error_message(context, "Unable to update because there is no key '20' in the treap"))

    def test_get_no_key_in_treap(self):
        node = TreapNode(10, "100")
        with self.assertRaises(KeyError) as context:
            node.get(20)

        self.assertTrue(check_error_message(context, "Key '20' isn't in the treap."))

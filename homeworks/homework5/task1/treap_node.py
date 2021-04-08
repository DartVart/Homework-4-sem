from random import random
from typing import Optional, Tuple, TypeVar, Generic, Iterator, cast, Any

from homeworks.homework5.task1.comparable import Comparable

K = TypeVar("K", bound=Comparable)
P = TypeVar("P", bound=Comparable)
V = Any


class TreapNode(Generic[K, P]):
    key: K
    value: V
    priority: P
    left: Optional["TreapNode[K, P]"]
    right: Optional["TreapNode[K, P]"]

    def __init__(
        self,
        key: K,
        value: V,
        priority: Optional[P] = None,
        left: Optional["TreapNode[K, P]"] = None,
        right: Optional["TreapNode[K, P]"] = None,
    ):
        self.key = key
        self.value = value
        cur_priority = random() if priority is None else priority
        self.priority = cast("P", cur_priority)
        self.left: Optional["TreapNode[K, P]"] = left
        self.right: Optional["TreapNode[K, P]"] = right

    def _merge(self, other: Optional["TreapNode[K, P]"]) -> "TreapNode[K, P]":
        """Combines two treaps into new one."""
        if other is None:
            return self

        if self.priority > other.priority:
            new_right = self.right._merge(other) if self.right is not None else other
            return TreapNode(self.key, self.value, self.priority, self.left, new_right)
        return TreapNode(other.key, other.value, other.priority, self._merge(other.left), other.right)

    def _split(self, key: K) -> Tuple[Optional["TreapNode[K, P]"], Optional["TreapNode[K, P]"]]:
        """
        Splits a treap by key.
        The node whose key is equal to the key along
        which splitting is going falls into the left subtreap.
        """

        new_treap, left, right = None, None, None

        if self.key > key:
            if self.left is not None:
                left, new_treap = self.left._split(key)
            right = TreapNode(self.key, self.value, self.priority, new_treap, self.right)
        else:
            if self.right is not None:
                new_treap, right = self.right._split(key)
            left = TreapNode(self.key, self.value, self.priority, self.left, new_treap)

        return left, right

    def _get_without_largest(self) -> Optional["TreapNode[K, P]"]:
        """Returns the subtreap without the largest key"""

        if self.right is not None:
            self.right = self.right._get_without_largest()
            return self

        # TODO: return self.left if self.left is not None else None
        return self.left

    def get_with_inserted(self, key: K, value: V, priority: Optional[P] = None) -> "TreapNode[K, P]":
        """Returns a treap with the inserted key"""

        left, right = self._split(key)
        new_node: "TreapNode[K, P]" = TreapNode(key, value, priority)
        if left is None:
            return new_node._merge(right)

        return left._merge(new_node)._merge(right)

    def get_with_removed(self, key: K) -> Optional["TreapNode[K, P]"]:
        """Returns a treap with the removed key"""

        left, right = self._split(key)
        if left is None:
            return right

        left = left._get_without_largest()
        if left is None:
            return right

        return left._merge(right)

    def update(self, key: K, value: V) -> None:
        """Updates the value for the key, doesn't insert a new one."""

        if self.key == key:
            self.value = value
        else:
            error_message = f"Unable to update because there is no key '{key}' in the treap."
            if key < self.key:
                if self.left is None:
                    raise KeyError(error_message)
                self.left.update(key, value)
            else:
                if self.right is None:
                    raise KeyError(error_message)
                self.right.update(key, value)

    def get(self, key: K) -> V:
        """Returns the value by key"""

        if self.key == key:
            return self.value

        error_message = f"Key '{key}' isn't in the treap."
        if key < self.key:
            if self.left is None:
                raise KeyError(error_message)
            return self.left.get(key)

        if self.right is None:
            raise KeyError(error_message)
        return self.right.get(key)

    def __contains__(self, key: K) -> bool:
        if self.key == key:
            return True

        if key < self.key:
            return self.left is not None and key in self.left

        return self.right is not None and key in self.right

    def __iter__(self) -> Iterator[K]:
        """Returns an iterator that traverses the keys in ascending order"""

        if self.left is not None:
            yield from self.left
        yield self.key
        if self.right is not None:
            yield from self.right

    def __reversed__(self) -> Iterator[K]:
        """Returns an iterator that traverses the keys in descending order"""

        if self.right is not None:
            yield from reversed(self.right)
        yield self.key
        if self.left is not None:
            yield from reversed(self.left)

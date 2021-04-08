from typing import MutableMapping, Iterator, Generic, TypeVar, cast, Any
from typing import Optional

from homeworks.homework5.task1.comparable import Comparable
from homeworks.homework5.task1.treap_node import TreapNode

K = TypeVar("K", bound=Comparable)
P = TypeVar("P", bound=Comparable)
V = Any


class Treap(MutableMapping[K, V], Generic[K, P]):
    _top: Optional["TreapNode[K, P]"]
    _length: int

    def __init__(self):
        self._length = 0
        self._top = None

    def __setitem__(self, key: K, value: V) -> None:
        if self._top is not None and key in self:
            self._top.update(key, value)
        else:
            if self._top is None:
                self._top = TreapNode(key, value)
            else:
                self._top = self._top.get_with_inserted(key, value)

            self._length += 1

    def insert(self, key: K, value: V, priority: P) -> None:
        """Inserts a new pair (key, value) with a priority."""

        if key in self:
            raise KeyError(f"The key '{key}' is already in the tree")

        if self._top is None:
            self._top = TreapNode(key, value)
        else:
            self._top = self._top.get_with_inserted(key, value, priority)

        self._length += 1

    def __delitem__(self, key: K) -> None:
        if self._top is None:
            raise KeyError("Treap is empty.")

        if key not in self:
            raise KeyError(f"Key '{key}' isn't in the treap.")

        self._top = self._top.get_with_removed(key)

        self._length -= 1

    def __getitem__(self, key: K) -> V:
        if self._top is None:
            raise KeyError("Treap is empty.")

        if key not in self:
            raise KeyError(f"Key '{key}' isn't in the treap.")

        return self._top.get(key)

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[K]:
        """Returns an iterator that traverses the keys in ascending order"""

        if self._top is None:
            yield from ()
        else:
            yield from self._top

    def __reversed__(self) -> Iterator[K]:
        """Returns an iterator that traverses the keys in descending order"""

        if self._top is None:
            yield from ()
        else:
            yield from reversed(self._top)

    # mypy requires the argument to be of type "object" ("Any") to match the "Mapping" supertype
    def __contains__(self, key: Any) -> bool:
        return self._top is not None and cast("K", key) in self._top

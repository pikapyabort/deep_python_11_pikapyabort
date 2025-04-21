# pylint: disable=R0903
class DoublyLinkedList:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    __slots__ = ("_capacity", "_map", "_head", "_tail")

    def __init__(self, limit: int = 34):
        if limit <= 0:
            raise ValueError("limit must be positive")
        self._capacity = limit
        self._map: dict = {}
        self._head: DoublyLinkedList | None = None
        self._tail: DoublyLinkedList | None = None

    def _add_front(self, x: DoublyLinkedList):
        x.prev = None
        x.next = self._head
        if self._head:
            self._head.prev = x
        self._head = x
        if self._tail is None:
            self._tail = x

    def _unlink(self, x: DoublyLinkedList):
        if x.prev:
            x.prev.next = x.next
        if x.next:
            x.next.prev = x.prev
        if x is self._head:
            self._head = x.next
        if x is self._tail:
            self._tail = x.prev
        x.prev = x.next = None

    def _move_front(self, x: DoublyLinkedList):
        if x is self._head:
            return
        self._unlink(x)
        self._add_front(x)

    def get(self, key):
        x = self._map.get(key)
        if x is None:
            return None
        self._move_front(x)
        return x.value

    def set(self, key, value):
        if key in self._map:
            x = self._map[key]
            x.value = value
            self._move_front(x)
            return
        x = DoublyLinkedList(key, value)
        self._map[key] = x
        self._add_front(x)
        if len(self._map) > self._capacity:
            tail = self._tail
            self._unlink(tail)
            del self._map[tail.key]

    def __getitem__(self, key):
        x = self._map[key]
        self._move_front(x)
        return x.value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self._map

    def __len__(self):
        return len(self._map)

    def __repr__(self):
        vals = []
        x = self._head
        while x:
            vals.append(f"{x.key}:{x.value}")
            x = x.next
        return f"LRUCache([{', '.join(vals)}])"

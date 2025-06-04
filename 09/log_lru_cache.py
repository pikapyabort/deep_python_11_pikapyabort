# pylint: disable=too-few-public-methods
# pylint: disable=duplicate-code
from __future__ import annotations
import argparse
import logging
from pathlib import Path


LOG_FILE = Path(__file__).with_name("cache.log")


class EvenWordsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return len(str(record.getMessage()).split()) % 2 == 1


def configure_logging(use_stdout: bool, use_filter: bool) -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        filemode="w",
        level=logging.DEBUG,
        format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s",
        force=True,
    )

    if use_stdout:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(
            "STD %(levelname)s → %(message)s"))
        logging.getLogger().addHandler(console)

    if use_filter:
        for h in logging.getLogger().handlers:
            h.addFilter(EvenWordsFilter())


class DoublyLinkedList:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    __slots__ = ("_capacity", "_map", "_head", "_tail", "_log")

    def __init__(self, limit: int = 34):
        if limit <= 0:
            raise ValueError("limit must be positive")
        self._capacity = limit
        self._map: dict = {}
        self._head: DoublyLinkedList | None = None
        self._tail: DoublyLinkedList | None = None
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("cache created with capacity=%s", limit)

    def _add_front(self, x: DoublyLinkedList) -> None:
        x.prev, x.next = None, self._head
        if self._head:
            self._head.prev = x
        self._head = x
        if self._tail is None:
            self._tail = x

    def _unlink(self, x: DoublyLinkedList) -> None:
        if x.prev:
            x.prev.next = x.next
        if x.next:
            x.next.prev = x.prev
        if x is self._head:
            self._head = x.next
        if x is self._tail:
            self._tail = x.prev
        x.prev = x.next = None

    def _move_front(self, x: DoublyLinkedList) -> None:
        if x is self._head:
            return
        self._unlink(x)
        self._add_front(x)

    def get(self, key):
        x = self._map.get(key)
        if x is None:
            self._log.warning("get absent key %r", key)
            return None
        self._move_front(x)
        self._log.info("get existing key %r -> %r", key, x.value)
        return x.value

    def set(self, key, value):
        if key in self._map:
            x = self._map[key]
            old_val = x.value
            x.value = value
            self._move_front(x)
            self._log.info("set existing key %r: %r → %r", key, old_val, value)
            return

        if len(self._map) == self._capacity:
            assert self._tail is not None
            self._log.warning(
                "capacity reached – evict key %r with value %r",
                self._tail.key, self._tail.value
            )
            tail = self._tail
            self._unlink(tail)
            del self._map[tail.key]

        x = DoublyLinkedList(key, value)
        self._map[key] = x
        self._add_front(x)
        self._log.info("set new key %r = %r", key, value)

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


def test(cache: LRUCache) -> None:
    cache.set("a", 1)
    cache.set("b", 2)
    cache.get("a")
    cache.get("z")
    cache.set("b", 22)
    cache.set("c", 3)
    cache.set("d", 4)
    logger = logging.getLogger(cache.__class__.__name__)
    logger.debug("final state: %s", cache)


def parse_cli() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="LRUCache test with rich logging.")
    p.add_argument("-c", "--capacity",
                   type=int,
                   default=3,
                   help="cache capacity (default 3)")
    p.add_argument("-s", "--stdout",
                   action="store_true",
                   help="duplicate logs to stdout")
    p.add_argument(
        "-f",
        "--filter",
        action="store_true",
        help="apply EvenWordsFilter (skip records with even word count)",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_cli()
    configure_logging(args.stdout, args.filter)
    test(LRUCache(args.capacity))

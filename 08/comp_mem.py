# pylint: disable=too-few-public-methods
import time
import weakref
import gc


class C:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class S:
    __slots__ = ("x", "y")

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Value:
    def __init__(self, val):
        self.val = val


class W:
    def __init__(self, x, y) -> None:
        self.x = weakref.ref(x)
        self.y = weakref.ref(y)

    @property
    def x_val(self):
        return self.x()

    @x_val.setter
    def x_val(self, v):
        self.x = weakref.ref(v)


def compare(cls, n: int):
    gc.disable()
    values = [Value(i) for i in range(n)]
    t0 = time.perf_counter()
    objs = [cls(values[i], values[i]) for i in range(n)]
    t1 = time.perf_counter()
    r = 0
    for o in objs:
        if cls is W:
            r += o.x_val.val
        else:
            r += o.x.val
    t2 = time.perf_counter()
    for o in objs:
        if cls is W:
            o.x_val = Value(r)
        else:
            o.x = Value(r)
    t3 = time.perf_counter()
    gc.enable()
    return t1 - t0, t2 - t1, t3 - t2


if __name__ == "__main__":
    N = 1_000_000
    for i in (C, S, W):
        a, b, c = compare(i, N)
        print(
            f"{i.__name__:>6}  "
            f"create={a:.4f}s  "
            f"read={b:.4f}s  "
            f"write={c:.4f}s"
        )

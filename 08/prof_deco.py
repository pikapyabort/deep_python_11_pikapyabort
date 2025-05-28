import cProfile
import functools
import io
import pstats


def profile_deco(fn):
    pr = cProfile.Profile()

    @functools.wraps(fn)
    def inner(*a, **kw):
        pr.enable()
        r = fn(*a, **kw)
        pr.disable()
        return r

    def print_stat():
        s = io.StringIO()
        stats = pstats.Stats(pr, stream=s)
        stats.strip_dirs()
        stats.sort_stats("cumulative")
        stats.print_stats()
        print(s.getvalue())

    inner.print_stat = print_stat
    return inner


if __name__ == "__main__":

    @profile_deco
    def add(a, b):
        return a + b

    @profile_deco
    def sub(a, b):
        return a - b

    for _ in range(1_000_000):
        add(1, 2)
        sub(4, 5)

    add.print_stat()
    sub.print_stat()

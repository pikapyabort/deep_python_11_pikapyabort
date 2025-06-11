import json
import random
import string
import time
import custom_json


def big():
    d = {}
    for _ in range(100_000):
        k = "".join(random.choices(string.ascii_letters, k=8))
        v = random.randint(0, 100_000)
        d[k] = v
    return d


def bench(fn, arg):
    t0 = time.perf_counter()
    fn(arg)
    return time.perf_counter() - t0


def test_speed():
    data = big()
    s_std = bench(json.dumps, data)
    s_cus = bench(custom_json.dumps, data)
    assert s_cus < s_std * 0.8

    j_std = bench(json.loads, json.dumps(data))
    j_cus = bench(custom_json.loads, json.dumps(data))
    assert j_cus < j_std * 0.6

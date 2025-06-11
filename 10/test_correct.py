import json
import random
import string
import pytest
import custom_json


def gen():
    d = {}
    for _ in range(100):
        k = "".join(random.choices(string.ascii_letters, k=6))
        v = random.choice([random.randint(-1_000, 1_000), k[::-1]])
        d[k] = v
    return d


@pytest.mark.parametrize("data", [gen() for _ in range(100)])
def test_roundtrip(data):
    s = custom_json.dumps(data)
    assert custom_json.loads(s) == data
    assert json.loads(s) == data


def test_invalid():
    with pytest.raises(TypeError):
        custom_json.loads("[1,2,3]")
    with pytest.raises(TypeError):
        custom_json.dumps(["not", "a", "dict"])

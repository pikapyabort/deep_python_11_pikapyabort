import pytest
from lru_cache import LRUCache


def test_interface_example():
    cache = LRUCache(2)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    assert cache.get("k3") is None
    assert cache.get("k2") == "v2"
    assert cache.get("k1") == "v1"
    cache.set("k3", "v3")
    assert cache.get("k3") == "v3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "v1"


@pytest.mark.parametrize(
    "cap, exc", [(0, ValueError), (-1, ValueError)]
)
def test_bad_capacity(cap, exc):
    with pytest.raises(exc):
        LRUCache(cap)


def test_len_and_contains():
    cache = LRUCache(3)
    cache.set("a", 1)
    cache.set("b", 2)
    assert len(cache) == 2
    assert "a" in cache and "c" not in cache


def test_update_existing_keeps_size():
    cache = LRUCache(1)
    cache.set("x", 1)
    cache.set("x", 2)
    assert cache.get("x") == 2
    assert len(cache) == 1


def test_dict_like_api():
    cache = LRUCache(2)
    cache["q"] = 7
    assert cache["q"] == 7
    cache["w"] = 8
    with pytest.raises(KeyError):
        _ = cache["e"]


def test_repr_has_keys():
    cache = LRUCache(2)
    cache.set("x", 1)
    cache.set("y", 2)
    t = repr(cache)
    assert "x:1" in t and "y:2" in t


def test_move_front_hits_x_next_branch():
    c = LRUCache(3)
    for k in ("a", "b", "c"):
        c.set(k, k)
    assert c.get("b") == "b"
    assert repr(c).startswith("LRUCache([b:")

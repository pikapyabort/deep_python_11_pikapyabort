import pytest
from descriptors import Data, Integer, String, PositiveInteger


def test_data_valid():
    d = Data(num=42, name="Answer", price=100)
    assert d.num == 42
    assert d.name == "Answer"
    assert d.price == 100


@pytest.mark.parametrize(
    "kwargs, exc_cls",
    [
        ({"num": "forty two", "name": "Test", "price": 10}, TypeError),
        ({"num": 1, "name": 123, "price": 10}, TypeError),
        ({"num": 1, "name": "Name", "price": 0}, ValueError),
        ({"num": 1, "name": "Name", "price": -1}, ValueError),
    ],
    ids=[
        "num-wrong-type",
        "name-wrong-type",
        "price-non-positive-zero",
        "price-non-positive-negative",
    ],
)
def test_data_invalid_creation(kwargs, exc_cls):
    with pytest.raises(exc_cls):
        Data(**kwargs)


def test_reassignment_valid():
    d = Data(num=10, name="Hi", price=1)
    d.num = 999
    d.name = "World"
    d.price = 5
    assert d.num == 999
    assert d.name == "World"
    assert d.price == 5


@pytest.mark.parametrize(
    "field, bad_value, exc_cls",
    [
        ("num", "str", TypeError),
        ("name", 1234, TypeError),
        ("price", 0, ValueError),
    ],
    ids=["num-bad", "name-bad", "price-bad"],
)
def test_reassignment_invalid_does_not_mutate(field, bad_value, exc_cls):
    original = Data(num=10, name="Ok", price=10)
    old_val = getattr(original, field)
    with pytest.raises(exc_cls):
        setattr(original, field, bad_value)
    assert getattr(original, field) == old_val


def test_deletion_forbidden():
    d = Data(1, "some", 10)
    with pytest.raises(AttributeError):
        del d.num
    with pytest.raises(AttributeError):
        del d.name
    with pytest.raises(AttributeError):
        del d.price


def test_descriptor_get_via_class():
    assert isinstance(Data.num, Integer)
    assert isinstance(Data.name, String)
    assert isinstance(Data.price, PositiveInteger)


def test_data_repr():
    d = Data(1, "test", 10)
    assert repr(d) == "Data(num=1, name='test', price=10)"


def test_instance_independence():
    first = Data(num=1, name="one", price=10)
    second = Data(num=2, name="two", price=20)
    assert (first.num, first.name, first.price) == (1, "one", 10)
    second.num = 200
    second.name = "changed"
    second.price = 300
    assert (first.num, first.name, first.price) == (1, "one", 10)
    assert (second.num, second.name, second.price) == (200, "changed", 300)

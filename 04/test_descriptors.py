import pytest
from descriptors import Data, Integer, String, PositiveInteger


def test_data_valid():
    d = Data(num=42, name="Answer", price=100)
    assert d.num == 42
    assert d.name == "Answer"
    assert d.price == 100


def test_data_invalid_num_type():
    with pytest.raises(TypeError):
        Data(num="forty two", name="Test", price=10)


def test_data_invalid_name_type():
    with pytest.raises(TypeError):
        Data(num=1, name=123, price=10)


def test_data_invalid_price_value():
    with pytest.raises(ValueError):
        Data(num=1, name="Name", price=0)
    with pytest.raises(ValueError):
        Data(num=1, name="Name", price=-1)


def test_reassignment_valid():
    d = Data(num=10, name="Hi", price=1)
    d.num = 999
    d.name = "World"
    d.price = 5
    assert d.num == 999
    assert d.name == "World"
    assert d.price == 5


def test_reassignment_invalid():
    d = Data(num=10, name="Ok", price=10)
    with pytest.raises(TypeError):
        d.num = "str"
    with pytest.raises(TypeError):
        d.name = 1234
    with pytest.raises(ValueError):
        d.price = 0


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

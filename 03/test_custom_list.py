import pytest
from custom_list import CustomList


def test_initialization():
    obj_empty = CustomList()
    assert isinstance(obj_empty, CustomList)
    assert obj_empty == CustomList([])
    obj_int = CustomList([1, 2, 3])
    assert isinstance(obj_int, CustomList)
    assert obj_int == CustomList([1, 2, 3])
    obj_single = CustomList([-42])
    assert isinstance(obj_single, CustomList)
    assert obj_single == CustomList([-42])


def test_add_custom_list():
    obj1 = CustomList([5, 1, 3, 7])
    obj2 = CustomList([1, 2, 7])
    obj1_copy = CustomList(obj1.copy())
    obj2_copy = CustomList(obj2.copy())
    result1 = obj1 + obj2
    assert isinstance(result1, CustomList)
    assert result1 == CustomList([6, 3, 10, 7])
    assert obj1 == obj1_copy
    assert obj2 == obj2_copy


def test_add_list():
    obj = CustomList([10])
    lst = [2, 5]
    obj_copy = CustomList(obj.copy())
    lst_copy = list(lst.copy())
    result1 = obj + lst
    result2 = lst + obj
    assert isinstance(result1, CustomList)
    assert result1 == CustomList([12, 5])
    assert isinstance(result2, CustomList)
    assert result2 == CustomList([12, 5])
    assert obj == obj_copy
    assert lst == lst_copy


def test_add_int():
    obj = CustomList([2, 5])
    obj_copy = CustomList(obj.copy())
    result1 = obj + 10
    result2 = 10 + obj
    assert isinstance(result1, CustomList)
    assert result1 == CustomList([12, 15])
    assert isinstance(result2, CustomList)
    assert result2 == CustomList([12, 15])
    assert obj == obj_copy


def test_sub_custom_list():
    obj1 = CustomList([5, 1, 3, 7])
    obj2 = CustomList([1, 2, 7])
    obj1_copy = CustomList(obj1.copy())
    obj2_copy = CustomList(obj2.copy())
    result = obj1 - obj2
    assert isinstance(result, CustomList)
    assert result == CustomList([4, -1, -4, 7])
    assert obj1 == obj1_copy
    assert obj2 == obj2_copy


def test_sub_list():
    obj = CustomList([10])
    lst = [2, 5]
    obj_copy = CustomList(obj.copy())
    lst_copy = list(lst.copy())
    result1 = obj - lst
    result2 = lst - obj
    assert isinstance(result1, CustomList)
    assert result1 == CustomList([8, -5])
    assert isinstance(result2, CustomList)
    assert result2 == CustomList([-8, 5])
    assert obj == obj_copy
    assert lst == lst_copy


def test_sub_int():
    obj = CustomList([2, 5])
    obj_copy = CustomList(obj.copy())
    result1 = obj - 10
    result2 = 10 - obj
    assert isinstance(result1, CustomList)
    assert result1 == CustomList([-8, -5])
    assert isinstance(result2, CustomList)
    assert result2 == CustomList([8, 5])
    assert obj == obj_copy


def test_eq():
    obj1 = CustomList([1, 2, 3])
    obj2 = CustomList([3, 3])
    assert obj1 == obj2


def test_lt():
    obj1 = CustomList([1, 2])
    obj2 = CustomList([4])
    assert obj1 < obj2
    assert obj1 <= obj2
    assert obj1 != obj2


def test_gt():
    obj1 = CustomList([2, 3])
    obj2 = CustomList([1, 1])
    assert obj1 > obj2
    assert obj1 >= obj2
    assert obj1 != obj2


def test_str():
    c1 = CustomList([2, 5])
    output = str(c1)
    assert "CustomList" in output
    assert "[2, 5]" in output
    assert "sum = 7" in output


def test_empty_list():
    obj_cl = CustomList([6, 6, 6])
    obj_emp = CustomList([])
    obj_ls = [6, 6, 6]
    result1 = obj_cl + obj_emp
    result2 = obj_emp - obj_cl
    result3 = obj_ls - obj_emp
    result4 = obj_emp + 5
    result5 = obj_emp + obj_emp
    assert isinstance(result1, CustomList)
    assert result1 == CustomList([6, 6, 6])
    assert isinstance(result2, CustomList)
    assert result2 == CustomList([-6, -6, -6])
    assert isinstance(result3, CustomList)
    assert result3 == CustomList([6, 6, 6])
    assert isinstance(result4, CustomList)
    assert result4 == CustomList([])
    assert isinstance(result5, CustomList)
    assert result5 == CustomList([])


def test_invalid_operations():
    with pytest.raises(TypeError):
        _ = CustomList([1]) + "str"
    with pytest.raises(TypeError):
        _ = 29.2 + CustomList([1])
    with pytest.raises(TypeError):
        _ = CustomList([1]) - 29.2
    with pytest.raises(TypeError):
        _ = "str" - CustomList([1])
    with pytest.raises(TypeError):
        _ = "str" == CustomList([1])
    with pytest.raises(TypeError):
        _ = "str" != CustomList([1])
    with pytest.raises(TypeError):
        _ = "str" < CustomList([1])
    with pytest.raises(TypeError):
        _ = "str" <= CustomList([1])
    with pytest.raises(TypeError):
        _ = "str" > CustomList([1])
    with pytest.raises(TypeError):
        _ = "str" >= CustomList([1])

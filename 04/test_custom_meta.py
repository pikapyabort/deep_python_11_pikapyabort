from custom_meta import CustomClass


# pylint: disable=no-member
def test_class_attributes():
    assert hasattr(CustomClass, 'custom_x')
    assert not hasattr(CustomClass, 'x')
    assert CustomClass.custom_x == 50


def test_instance_attributes():
    inst = CustomClass()
    assert hasattr(inst, 'custom_x')
    assert inst.custom_x == 50
    assert hasattr(inst, 'custom_val')
    assert inst.custom_val == 99
    assert hasattr(inst, 'custom_line')
    assert inst.custom_line() == 100
    assert str(inst) == "Custom_by_metaclass"
    assert not hasattr(inst, 'x')
    assert not hasattr(inst, 'val')
    assert not hasattr(inst, 'line')
    assert not hasattr(inst, 'yyy')


def test_dynamic_attribute():
    inst = CustomClass()
    inst.dynamic = "added later"
    assert hasattr(inst, 'custom_dynamic')
    assert not hasattr(inst, 'dynamic')
    assert inst.custom_dynamic == "added later"


def test_initialization_with_different_values():
    inst = CustomClass(val=123)
    assert inst.custom_val == 123
    assert not hasattr(inst, 'val')
    assert hasattr(inst, 'custom_val')


def test_magic_name_behavior():
    inst = CustomClass()
    inst.__magic__ = 999
    assert hasattr(inst, '__magic__')
    assert not hasattr(inst, 'custom___magic__')
    assert inst.__magic__ == 999

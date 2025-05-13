from abc import ABC, abstractmethod


# pylint: disable=R0903
class BaseDescriptor(ABC):
    def __init__(self):
        super().__init__()
        self._attr_name = None

    def __set_name__(self, owner, name):
        self._attr_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._attr_name, None)

    def __set__(self, instance, value):
        try:
            self.validate(value)
        except (TypeError, ValueError) as exc:
            raise exc.__class__(f"Поле '{self._attr_name}': {exc}") from None
        instance.__dict__[self._attr_name] = value

    def __delete__(self, instance):
        raise AttributeError(f"Нельзя удалять атрибут '{self._attr_name}'")

    @abstractmethod
    def validate(self, value):  # pragma: no cover
        pass


class Integer(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f"Значение должно быть int, получено {type(value).__name__}"
            )


class String(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f"Значение должно быть str, получено {type(value).__name__}"
            )


class PositiveInteger(Integer):
    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError(
                "Значение должно быть положительным, "
                f"получено {value}"
            )


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Data(num={self.num}, name={self.name!r}, price={self.price})"

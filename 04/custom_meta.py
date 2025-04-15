class AddPrefixMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        new_dict = {}
        for attr_name, attr_value in classdict.items():
            if attr_name.startswith('__') and attr_name.endswith('__'):
                new_dict[attr_name] = attr_value
            else:
                new_dict['custom_' + attr_name] = attr_value
        cls = super().__new__(mcs, name, bases, new_dict, **kwargs)

        def new_setattr(self, name, value):
            if name.startswith('__') and name.endswith('__'):
                object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, 'custom_' + name, value)

        cls.__setattr__ = new_setattr
        return cls


class CustomClass(metaclass=AddPrefixMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

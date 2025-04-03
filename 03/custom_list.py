class CustomList(list):

    def __add__(self, other):
        if isinstance(other, int):
            return CustomList(x + other for x in self)
        if isinstance(other, list):
            max_len = max(len(self), len(other))
            new_data = []
            for i in range(max_len):
                val_self = self[i] if i < len(self) else 0
                val_other = other[i] if i < len(other) else 0
                new_data.append(val_self + val_other)
            return CustomList(new_data)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, int):
            return CustomList(x + other for x in self)
        if isinstance(other, list):
            max_len = max(len(self), len(other))
            new_data = []
            for i in range(max_len):
                val_self = self[i] if i < len(self) else 0
                val_other = other[i] if i < len(other) else 0
                new_data.append(val_other + val_self)
            return CustomList(new_data)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, int):
            return CustomList(x - other for x in self)
        if isinstance(other, list):
            max_len = max(len(self), len(other))
            new_data = []
            for i in range(max_len):
                val_self = self[i] if i < len(self) else 0
                val_other = other[i] if i < len(other) else 0
                new_data.append(val_self - val_other)
            return CustomList(new_data)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return CustomList(other - x for x in self)
        if isinstance(other, list):
            max_len = max(len(self), len(other))
            new_data = []
            for i in range(max_len):
                val_self = self[i] if i < len(self) else 0
                val_other = other[i] if i < len(other) else 0
                new_data.append(val_other - val_self)
            return CustomList(new_data)
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        return sum(self) == sum(other)

    def __ne__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        return sum(self) != sum(other)

    def __lt__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        return sum(self) < sum(other)

    def __le__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        return sum(self) <= sum(other)

    def __gt__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        return sum(self) > sum(other)

    def __ge__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        return sum(self) >= sum(other)

    def __str__(self):
        return f"{type(self).__name__}({list(self)}), sum = {sum(self)}"

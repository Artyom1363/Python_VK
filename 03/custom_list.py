"""
this module provide custom list
"""


class CustomList(list):
    """
    this is custom list
    """
    def __eq__(self, other) -> bool:
        return sum(self) == sum(other)

    def __add__(self, other):
        self_copy = self.copy()
        len_self_copy = len(self_copy)
        for i, value in enumerate(other):
            if i < len_self_copy:
                self_copy[i] += value
            else:
                self_copy.append(value)
        return self_copy

    def __radd__(self, other):
        self_copy = self.copy()
        len_self_copy = len(self_copy)
        for i, value in enumerate(other):
            if i < len_self_copy:
                self_copy[i] += value
            else:
                self_copy.append(value)
        return self_copy

    def __sub__(self, other):
        self_copy = self.copy()
        len_self_copy = len(self_copy)
        for i, value in enumerate(other):
            if i < len_self_copy:
                self_copy[i] -= value
            else:
                self_copy.append(-value)
        return self_copy

    def __rsub__(self, other):
        self_copy = self.copy()
        len_self_copy = len(self_copy)
        for i, value in enumerate(other):
            if i < len_self_copy:
                self_copy[i] = value - self_copy[i]
            else:
                self_copy.append(value)
        return self_copy

    def __str__(self) -> str:
        return super().__str__() + " sum: " + str(sum(self))

"""
this module provide custom list
"""
from itertools import zip_longest

class CustomList(list):
    """
    this is custom list
    """
    def __eq__(self, other) -> bool:
        return sum(self) == sum(other)

    def __add__(self, other):
        return_list = CustomList()
        for a, b in zip_longest(self, other, fillvalue=0):
            return_list.append(a + b)
        return return_list

    def __radd__(self, other):
        return self.__class__.__add__(self, other)

    def __sub__(self, other):
        return_list = CustomList()
        for a, b in zip_longest(self, other, fillvalue=0):
            return_list.append(a - b)
        return return_list

    def __rsub__(self, other):
        return_list = CustomList()
        for a, b in zip_longest(self, other, fillvalue=0):
            return_list.append(b - a)
        return return_list

    def __str__(self) -> str:
        return super().__str__() + " sum: " + str(sum(self))

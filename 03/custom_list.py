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
        for self_el, other_el in zip_longest(self, other, fillvalue=0):
            return_list.append(self_el + other_el)
        return return_list

    def __radd__(self, other):
        return self.__class__.__add__(self, other)

    def __sub__(self, other):
        return_list = CustomList()
        for self_el, other_el in zip_longest(self, other, fillvalue=0):
            return_list.append(self_el - other_el)
        return return_list

    def __rsub__(self, other):
        return_list = CustomList()
        for self_el, other_el in zip_longest(self, other, fillvalue=0):
            return_list.append(other_el - self_el)
        return return_list

    def __str__(self) -> str:
        return super().__str__() + " sum: " + str(sum(self))

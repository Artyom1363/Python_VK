class Integer:

    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, obj, objtype):
        return getattr(obj, self.field_name)

    def __set__(self, obj, val):
        if isinstance(val, int):
            setattr(obj, self.field_name, val)
        else:
            raise ValueError("Invalid data for datatype int")


class String:
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, obj, objtype):
        return getattr(obj, self.field_name)

    def __set__(self, obj, val):
        if isinstance(val, str):
            setattr(obj, self.field_name, val)
        else:
            raise ValueError("Invalid data for datatype string")


class PositiveInteger:
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, obj, objtype):
        return getattr(obj, self.field_name)

    def __set__(self, obj, val):
        if isinstance(val, int) and val >= 0:
            setattr(obj, self.field_name, val)
        else:
            raise ValueError("Invalid data for datatype positive int")

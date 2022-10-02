

class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        def _setattr_(self, name, value):
            custom_name = "custom_" + name
            object.__setattr__(self, custom_name, value)

        custom_classdict = {}
        for method in classdict:
            if method[0:2] == "__" and method[-2:] == "__":
                custom_classdict[method] = classdict[method]
            else:
                custom_method = "custom_" + method
                custom_classdict[custom_method] = classdict[method]

        custom_classdict["__setattr__"] = _setattr_
        cls = super().__new__(mcs, name, bases, custom_classdict, **kwargs)

        return cls

    def __init__(cls, name, bases, classdict, **kwargs):
        super().__init__(name, bases, classdict, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    @classmethod
    def __prepare__(mcs, cls, bases, **extra_kwargs):
        prepared_data = super().__prepare__(mcs, cls, bases, **extra_kwargs)
        return prepared_data

import functools
from functools import partial


class Accessor:

    def __init__(self, inst, type_):
        self.inst = inst
        self.type = type_

    def __getattr__(self, item):
        cls_dict = type(self.inst).__dict__
        for k, v in cls_dict.items():
            if k.strip('_') == item:
                func = cls_dict[k]
                if func.type == self.type:
                    return partial(func, self.inst)
        raise AttributeError(
            f'Could not find function {item} in {type(self).__name__} \'{self.type}\'')


class noclashdict(dict):

    def __setitem__(self, name, value):
        while name in self:
            name += '_'
        super().__setitem__(name, value)


class MarkableMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        # https://groups.google.com/d/msg/comp.lang.python/rQjrnrg6TmE/JG_u2E2oap0J
        return noclashdict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        obj.__getattr__ = lambda inst, type_: Accessor(inst, type_)
        return obj

    def __getattr__(cls, key):
        def f(func):
            func.type = key
            func.__name__ = f'{key}.{func.__name__}'
            return func

        return f


class MarkMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        # https://groups.google.com/d/msg/comp.lang.python/rQjrnrg6TmE/JG_u2E2oap0J
        return noclashdict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        obj.__getattr__ = lambda inst, type_: Accessor(inst, type_)
        return obj


class mark(metaclass=MarkMeta):

    def __init__(self, type_):
        self.type = type_

    def __call__(self, func):
        func.type = self.type
        func.__name__ = f'{self.type}.{func.__name__}'
        return func


class Markable(metaclass=MarkableMeta):
    pass

# def mark(key):
#
#     def outter(func):
#         @functools.wraps(func)
#         def wrapper(inst, *args, **kwargs):
#

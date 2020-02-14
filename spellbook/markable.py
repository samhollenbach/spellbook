from functools import partial
from types import MethodType


# def markable(cls):
#     for name, attr in cls.__dict__.items():
#         poop = getattr(attr, 'group', None)
#         print('~', poop)
#     return cls


class AccessorNew:
    def __init__(self, group):
        self.group = group
        self.instance = None
        self.owner = None

    def __get__(self, instance, owner):
        self.instance = instance
        self.owner = owner
        return self

    def __getattr__(self, item):
        for name, func in self.owner.__dict__.items():
            if name.strip('_') == item:
                if func.group == self.group:
                    return MethodType(func, self.instance)
        raise AttributeError(
            f"Could not find function {item} in {type(self).__name__} '{self.group}'")


class Accessor:

    def __init__(self, inst, group):
        self.inst = inst
        self.group = group

    def __getattr__(self, item):
        cls_dict = type(self.inst).__dict__
        for name, func in cls_dict.items():
            print('$', name, item)
            if name.strip('_') == item:
                if func.group == self.group:
                    return MethodType(func, self.inst)
        raise AttributeError(
            f"Could not find function {item} in {type(self).__name__} '{self.group}'")


class noclashdict(dict):

    def __setitem__(self, name, value):
        while name in self:
            name += '_'
        super().__setitem__(name, value)


class MarkMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        # https://groups.google.com/d/msg/comp.lang.python/rQjrnrg6TmE/JG_u2E2oap0J
        return noclashdict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        obj.__getattr__ = lambda inst, group: Accessor(inst, group)
        return obj


class MarkMetaNew(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        # https://groups.google.com/d/msg/comp.lang.python/rQjrnrg6TmE/JG_u2E2oap0J
        return noclashdict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        for name, attr in obj.__dict__.copy().items():
            group = getattr(attr, 'group', None)
            if group:
                setattr(obj, group, Accessor(group))
        return obj


class Markable(metaclass=MarkMeta):
    """Use as the super class"""

    def list_groups(self):
        groups = set()
        for attr in type(self).__dict__.values():
            if callable(attr) and hasattr(attr, 'group'):
                groups.add(attr.group)
        return groups


def mark(group):
    def decorator(func):
        func.group = group
        func.__name__ = f'{group}.{func.__name__}'
        return func
    return decorator


class Testable(Markable):
    @mark('foo')
    def bar(self):
        return 42

    @mark('goo')
    def bar(self):
        return 804


if __name__ == '__main__':
    t = Testable()
    t.poop = 1
    t2 = Testable()
    t2.poop = 2
    f = t.foo

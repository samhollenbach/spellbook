from functools import partial


class Accessor:

    def __init__(self, inst, type_):
        self.inst = inst
        self.type = type_

    def __getattr__(self, item):
        bases = type(self.inst).__mro__
        for base in bases:
            cls_dict = base.__dict__

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


class MarkMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        # https://groups.google.com/d/msg/comp.lang.python/rQjrnrg6TmE/JG_u2E2oap0J
        return noclashdict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        obj.__getattr__ = lambda inst, type_: Accessor(inst, type_)
        return obj


class Markable(metaclass=MarkMeta):
    """Use as the super class"""

    def list(self):
        types = set()
        cls = type(self)
        for k, v in cls.__dict__.items():
            if callable(v) and hasattr(v, 'type'):
                types.add(v.type)
        return types


class mark:
    """The decorator"""

    def __init__(self, type_):
        self.type = type_

    def __call__(self, func):
        func.type = self.type
        func.__name__ = f'{self.type}.{func.__name__}'
        return func

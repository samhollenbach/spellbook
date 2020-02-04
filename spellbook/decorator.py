from functools import partial


class RegistryMeta(type):

    def __getattr__(cls, key):
        print(key)

        def f(func):
            func.type = key
            return func

        return f


class Registry(metaclass=RegistryMeta):
    pass


class PropStore:

    def __init__(self, inst, type_):
        self.inst = inst
        self.type = type_
        self.d = {}

    def __getattr__(self, item):
        cls_dict = type(self.inst).__dict__
        for k, v in cls_dict.items():
            if k.strip() == item:
                func = cls_dict[k]
                if func.type == self.type:
                    return partial(func, self.inst)
        raise AttributeError


class noclashdict(dict):

    def __setitem__(self, name, value):
        setitem = super().__setitem__
        while name in self:
            name += ' '
        setitem(name, value)


class DecoratorMeta(type):

    @classmethod
    def __prepare__(cls, name, bases):
        # https://groups.google.com/d/msg/comp.lang.python/rQjrnrg6TmE/JG_u2E2oap0J
        return noclashdict()

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__getattr__ = lambda inst, type: PropStore(inst, type)
        return obj


class Test(metaclass=DecoratorMeta):

    def __init__(self):
        pass

    @Registry.handlers
    def test(self):
        print('I am hadlers')
        return 'wew'

    @Registry.emitters
    def test(self):
        print('I am emitter')

        h = self.handlers.test()
        print('emitter also get handle', h)
        return 'wew'


t = Test()

t.emitters.test()
t.handlers.test()

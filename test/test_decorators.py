from nose.tools import eq_, nottest
from spellbook.decorator import Decoratable


@nottest
class DecoratorTest(Decoratable):

    @Decoratable.handlers
    def test(self):
        return 'handler'

    @Decoratable.emitters
    def test(self):
        return 'emitter'


def test_decorators():
    t = DecoratorTest()

    t1 = t.handlers.test()
    t2 = t.emitters.test()
    eq_(t1, 'handler')
    eq_(t2, 'emitter')

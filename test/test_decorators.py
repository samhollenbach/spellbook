from nose.tools import eq_, nottest
from spellbook.markable import Markable, mark


@nottest
class MarkableTest(Markable):

    def __init__(self, val):
        self.val = val

    @mark('handlers')
    def test(self):
        return f'handler({self.val})'

    @mark('emitters')
    def test(self):
        return f'emitter({self.val})'


def test_decorable():
    dec_test1 = MarkableTest(1)

    t1 = dec_test1.handlers.test()
    e1 = dec_test1.emitters.test()
    eq_(t1, 'handler(1)')
    eq_(e1, 'emitter(1)')

    dec_test2 = MarkableTest(2)

    t2 = dec_test2.handlers.test()
    e2 = dec_test2.emitters.test()
    eq_(t2, 'handler(2)')
    eq_(e2, 'emitter(2)')

    t1b = dec_test1.handlers.test()
    e1b = dec_test1.emitters.test()
    eq_(t1b, 'handler(1)')
    eq_(e1b, 'emitter(1)')

    dec_test1.val = 3
    t1c = dec_test1.handlers.test()
    e1c = dec_test1.emitters.test()
    eq_(t1c, 'handler(3)')
    eq_(e1c, 'emitter(3)')

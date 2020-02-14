import asyncio

import functools


def retry(func, wait=3, retries=None, *args, **kwargs):
    r = None
    nretry = 0
    while not retries or nretry <= retries:
        r = func(*args, **kwargs)
        if r:
            break
        time.sleep(wait)
    return r


class waiter(object):
    WAIT = 'wait'
    RESPOND = 'respond'

    class dec:
        cache = {}
        hooks = set()

        def __init__(self, f, hook=None, type_=None, wait_time=5):
            functools.update_wrapper(self, f)
            if not hook or not type_:
                raise ValueError('put hook and type pls')
            self.f = f
            self.hook = hook
            self.hooks.add(hook)
            self.type = type_
            self.return_value = None
            self.cache[self.get_cache_name(type_)] = self.f
            self.wait_time = wait_time

        def get_cache_name(self, type_):
            return f'{self.hook}_{type_}'

        def __call__(self, *args, **kwargs):
            self.return_value = self.f(*args, **kwargs)
            if self.type == waiter.WAIT:
                responder_name = self.get_cache_name(waiter.RESPOND)
                responder_func = self.cache.get(responder_name)
                if not responder_func:
                    raise AttributeError(
                        f'wait({self.hook}) function {self.f.__name__} has no '
                        f'corresponding responder')

                responder_value = None
                started = time.time()
                while not self.wait_time or time.time() - started < self.wait_time:
                    responder_value = responder_func.return_value
                    if responder_value:
                        break
                return responder_value
            else:
                return self.return_value

        def __get__(self, obj, objtype):
            return functools.partial(self.__call__, obj)

    @classmethod
    def wait(cls, hook):
        return functools.partial(cls.dec, hook=hook, type_=cls.WAIT)

    @classmethod
    def respond(cls, hook):
        return functools.partial(cls.dec, hook=hook, type_=cls.RESPOND)


# class test:
#
#     def main(self, *args, **kwargs):
#         r = retry(self.call, *args, **kwargs)
#         # False: failed
#         # True: succeeded
#
#     @waiter.wait('test')
#     def call(self):
#         print('call!')
#         return 'anything'
#
#     @waiter.respond('test')
#     def resp(self):
#         print('resp!')
#         return True


class ran_wrapper(object):

    def __init__(self, f):
        self.f = f
        self.ran = False
        self.r_val = None

    def __call__(self, *args, **kwargs):
        self.r_val = self.f(*args, **kwargs)
        self.ran = True
        return self.r_val

    def __get__(self, instance, owner):
        pfunc = functools.partial(self.__call__, instance)
        pfunc.ran = self.ran
        pfunc.r_val = self.r_val
        return pfunc


class async_test:

    @ran_wrapper
    async def responder(self):
        print('responded')
        await asyncio.sleep(5)
        print('setting ran')
        return 'test'

    async def main(self):
        print('pubbed')
        p = await self.poll()
        return p

    async def poll(self):
        while not self.responder.ran:
            print('polled')
            await asyncio.sleep(1)
        return self.responder.r_val


async def emit(q: asyncio.Queue) -> None:
    print('adding to queue')
    await q.put(True)
    while not q.empty():
        print('looping')
        await asyncio.sleep(1)
    print('exiting emit')


async def react(q: asyncio.Queue) -> None:
    await asyncio.sleep(5)
    print('removing from queue')
    t = await q.get()
    return t


at = async_test()






async def main():
    q = asyncio.Queue()
    await asyncio.gather(emit(q), react(q))


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

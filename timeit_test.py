import functools
import time


#使用装饰器输出程序运行消耗的时间
def timeit_test(number=3, repeat=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(repeat):
                start = time.perf_counter()
                for _ in range(number):
                    func(*args, **kwargs)
                elapsed = (time.perf_counter() - start)
                print('Time of {} used: {} '.format(i, elapsed))

        return wrapper

    return decorator


@timeit_test(number=1, repeat=3)
def test():
    a = []
    for i in range(2000000):
        a.append(i)


test()
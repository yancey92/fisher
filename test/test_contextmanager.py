"""
    contextmanager 是 Python 中的一个上下文管理器装饰器，用于简化上下文管理器的创建过程。
    上下文管理器是一种用于管理资源的对象，它定义了在进入和离开代码块时应该执行的操作。
    
    使用 contextmanager 装饰器, 我们可以将一个生成器函数转换为上下文管理器。
    生成器函数使用 yield 语句将控制权交给上下文管理器, 使其在进入和离开代码块时执行相应的操作。
    
"""
from contextlib import contextmanager


class Test:
    def test(self):
        print("2:   into test fuction")


@contextmanager
def test_ctxmgr_fuction():
    print("1:   into test_ctxmgr_fuction")
    yield Test()
    print("4:   exit test_ctxmgr_fuction")


with test_ctxmgr_fuction() as ctxmgr:
    ctxmgr.test()
    print("3:   successful, exec end")

"""
dm02_retry - 

面试题：

问题：什么是装饰器？
回答：用一个函数去装饰另外一个函数或类并未其提供额外的能力（横切关注功能）：代理模式。

Author: poterliu
Version: 0.0.1
Date: 2026/10/26 
"""
import random
import time
from functools import wraps
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec('P')
R = TypeVar('R')

# 给装饰器写类型注释
def record_time(func: Callable[P, R]) -> Callable[P, R]:

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        ret_value = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Execute time: {end - start:.3f}s')
        return ret_value

    return wrapper



def retry(trys: int = 3, max_delay: int = 10, delay_factor: int = 2) -> Callable[P, R]:
    """
    重试装饰器
    :param trys: 重试次数
    :param max_delay: 最大延迟时间（避让时间）
    :param delay_factor: 延迟因子
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for i in range(trys):
                try:
                    ret_value = func(*args, **kwargs)
                    print(f'{func.__name__} 执行成功')
                    return ret_value
                except Exception as e:
                    print(f'{func.__name__} 执行失败，第 {i + 1} 次重试...')
                    if i < trys:
                        time.sleep(min(max_delay, delay_factor ** i))
            print(f'{func.__name__} 执行失败，{trys} 次重试后仍失败')
            # raise Exception(f'{func.__name__} 执行失败')
            return None

        return wrapper
    return decorator

# 语法糖（便捷语法、糖衣语法）
@retry(trys=3)
def foo() -> int:
    magic_number = random.randrange(1, 100)
    if random.random() < 0.5:
        raise ValueError("卵了")
    return magic_number


if __name__ == '__main__':
    print(foo())

    # @retry(trys=3) 的等价写法：需要移除foo()函数上的@retry(trys=3)，否则会retry 会执行两遍
    # fo = retry(trys=3)(foo)
    # print(fo())